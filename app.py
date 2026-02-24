from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
user_info = {
    'Andres': {'password': '123', 'role': 'Admin'},
    'Daniel':{'password': '456', 'role': 'User'}
    }

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    if name in user_info and user_info[name]['password'] == password:
        log = user_info.get(name)
        match log['role']:
            case "Admin":
                return render_template('Menu_Admin.html', name=name)
            case "User":
                return render_template('Menu_User.html', name=name)
    else:
        return render_template('index.html', error="Usuario o contraseña incorrectos")


@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('register.html', error="Las contraseñas no coinciden")
        
        if name in user_info:
            return render_template('register.html', error="El usuario ya existe")
        
        role = 'User'
        user_info[name] = {'password': password, 'role': role}
        return render_template('index.html', success="Usuario registrado exitosamente. Inicia sesión")
    else:
        return render_template('register.html')

@app.route('/products', methods=['GET'])
def products():
    products = [
        {'name': 'laptop', 'price': 10.99},
        {'name': 'motorolaG05', 'price': 15.49},
        {'name': 'samsung', 'price': 7.99}
    ].copy('products')
    return render_template('products.html', products=products)

@app.route('/admin')
def admin():
    return render_template('Menu_Admin.html')

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('index.html', success="Has cerrado sesión exitosamente")

if __name__ == '__main__':
    app.run(debug=True)