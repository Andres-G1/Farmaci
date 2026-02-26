from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "123"  # necesaria para usar session

user_info = {
    'Andres': {'password': '123', 'role': 'Admin'},
    'Daniel': {'password': '456', 'role': 'User'}
}

products_db = [
    {'id': 1, 'name': 'Aspirina', 'price': 5000, 'category': 'Medicamento'},
    {'id': 2, 'name': 'Shampoo', 'price': 8000, 'category': 'Aseo personal'},
    {'id': 3, 'name': 'Dolex', 'price': 4000, 'category': 'Medicamento'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'user' in session:
        if session.get('role') == 'Admin':
            return redirect(url_for('menu_admin'))
        return redirect(url_for('menu_user'))

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if name in user_info and user_info[name]['password'] == password:
            session['user'] = name
            session['role'] = user_info[name]['role']

            if session['role'] == "Admin":
                return redirect(url_for('menu_admin'))
            else:
                return redirect(url_for('menu_user'))

        return render_template('login.html', error="Usuario o contraseña incorrectos")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('login.html', error="Las contraseñas no coinciden")

        if name in user_info:
            return render_template('login.html', error="El usuario ya existe")

        user_info[name] = {'password': password, 'role': 'User'}
        return render_template('login.html', success="Usuario registrado exitosamente. Inicia sesión")

    return render_template('login.html')



@app.route('/menu_user')
def menu_user():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Menu_User.html', products=products_db)


@app.route('/Products')
def menu_produc():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Products.html', products=products_db)


@app.route('/menu_admin')
def menu_admin():
    if 'user' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    return render_template('Menu_Admin.html', products=products_db)


@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if 'user' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))

    name = request.form.get('name')
    price = request.form.get('price')
    category = request.form.get('category')

    new_id = products_db[-1]['id'] + 1 if products_db else 1

    products_db.append({
        'id': new_id,
        'name': name,
        'price': int(price),
        'category': category
    })

    return redirect(url_for('menu_admin'))


@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)