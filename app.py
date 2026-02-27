from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "2122022025"

# ─── DATA ──────────────────────────────────────────────
user_info = {
    'Andres': {'password': '123', 'role': 'Admin'},
    'Daniel': {'password': '456', 'role': 'User'}
}

products_db = [
    {'id': 1, 'name': 'Aspirina',  'price': 5000, 'category': 'Medicamento'},
    {'id': 2, 'name': 'Shampoo',   'price': 8000, 'category': 'Aseo personal'},
    {'id': 3, 'name': 'Dolex',     'price': 4000, 'category': 'Medicamento'},
]

# ─── INDEX ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ─── AUTH ──────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        if session.get('role') == 'Admin':
            return redirect(url_for('menu_admin'))
        return redirect(url_for('menu_user'))

    if request.method == 'POST':
        name     = request.form.get('name')
        password = request.form.get('password')

        if name in user_info and user_info[name]['password'] == password:
            session['user'] = name
            session['role'] = user_info[name]['role']
            return redirect(url_for('menu_admin') if session['role'] == 'Admin' else url_for('menu_user'))

        return render_template('login.html', error="Usuario o contraseña incorrectos")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name             = request.form.get('name')
        password         = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('login.html', error="Las contraseñas no coinciden")
        if name in user_info:
            return render_template('login.html', error="El usuario ya existe")

        user_info[name] = {'password': password, 'role': 'User'}
        return render_template('login.html', success="Usuario registrado exitosamente. Inicia sesión")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── USER ──────────────────────────────────────────────
@app.route('/menu_user')
def menu_user():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Menu_User.html', products=products_db)


# ─── PRODUCTS ──────────────────────────────────────────
@app.route('/Products')
def menu_produc():
    if 'user' not in session:
        return redirect(url_for('login'))

    categories = list(set(p['category'] for p in products_db))
    return render_template(
        'Products.html',
        products=products_db,
        categories=categories,
        query='',
        category_selected='',
        price_min=0,
        price_max=100000
    )


@app.route('/SearchP')
def productos_view():
    if 'user' not in session:
        return redirect(url_for('login'))

    query     = request.args.get('q', '')
    category  = request.args.get('category', '')
    price_min = request.args.get('price_min', 0,      type=int)
    price_max = request.args.get('price_max', 100000, type=int)

    result = products_db

    if query:
        result = [p for p in result if query.lower() in p['name'].lower()]
    if category:
        result = [p for p in result if p['category'] == category]
    result = [p for p in result if price_min <= p['price'] <= price_max]

    categories = list(set(p['category'] for p in products_db))

    return render_template(
        'Products.html',
        products=result,
        categories=categories,
        query=query,
        category_selected=category,
        price_min=price_min,
        price_max=price_max
    )

# ─── ADMIN ─────────────────────────────────────────────
@app.route('/menu_admin')
def menu_admin():
    if 'user' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))
    # Convertir dict a lista ordenada para el template
    users_list = [
        {'username': name, 'role': data['role']}
        for name, data in user_info.items()
    ]
    return render_template('Menu_Admin.html', products=products_db, users=users_list)


@app.route('/admin/add_product', methods=['POST'])
def add_product():
    if 'user' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))

    name     = request.form.get('name', '').strip()
    price    = request.form.get('price', 0)
    category = request.form.get('category', '').strip()

    if not name or not category:
        return redirect(url_for('menu_admin'))

    new_id = (products_db[-1]['id'] + 1) if products_db else 1
    products_db.append({
        'id': new_id,
        'name': name,
        'price': int(price),
        'category': category
    })
    return redirect(url_for('menu_admin'))


# ─── ADD USER (Admin) ───────────────────────────────────
@app.route('/admin/add_user', methods=['POST'])
def add_user():
    # 1. Solo admins pueden acceder
    if 'user' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login'))

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    role     = request.form.get('role', '').strip()

    # 2. Validar campos obligatorios
    if not username or not password or not role:
        return redirect(url_for('menu_admin'))

    # 3. Verificar que el usuario no exista ya
    #    user_info es dict → la clave ES el nombre de usuario
    if username in user_info:
        return redirect(url_for('menu_admin'))

    # 4. Agregar al diccionario con la misma estructura que ya existe
    user_info[username] = {
        'password': password,   # se guarda como string, igual que los demás
        'role': role
    }

    return redirect(url_for('menu_admin'))


# ─── RUN ───────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
