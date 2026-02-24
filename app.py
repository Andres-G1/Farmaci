from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


user_info = {
    'Andres': {'password': '123', 'role': 'Admin'},
    'Daniel': {'password': '456', 'role': 'User'}
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', error="Las contraseñas no coinciden")

        if name in user_info:
            return render_template('register.html', error="El usuario ya existe")

        user_info[name] = {'password': password, 'role': 'User'}
        return render_template('login.html', success="Usuario registrado exitosamente. Inicia sesión")

    return render_template('register.html')


@app.route('/products')
def products():
    products = [
        {'name': 'Laptop', 'price': 10.99},
        {'name': 'Motorola G05', 'price': 15.49},
        {'name': 'Samsung', 'price': 7.99}
    ]
    return render_template('products.html', products=products)


@app.route('/admin')
def admin():
    return render_template('Menu_Admin.html')

if __name__ == '__main__':
    app.run(debug=True)