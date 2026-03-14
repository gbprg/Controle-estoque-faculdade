from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db, init_db
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura_aqui'

# Inicializa o banco de dados no startup se não existir
if not os.path.exists('estoque.db'):
    init_db()

def is_admin():
    return session.get('role') == 'admin'

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    
    return render_template('dashboard.html', products=products, is_admin=is_admin())

@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Nome é um campo obrigatório.', 'danger')
            return redirect(url_for('cadastrar_produto'))
            
        try:
            quantity = int(request.form.get('quantity'))
            min_quantity = int(request.form.get('min_quantity'))
            price = float(request.form.get('price'))
        except (ValueError, TypeError):
            flash('Quantidade, Quantidade Mínima e Preço devem ser preenchidos e válidos numéricamente.', 'danger')
            return redirect(url_for('cadastrar_produto'))
            
        conn = get_db()
        conn.execute('''
            INSERT INTO products (name, description, quantity, min_quantity, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, quantity, min_quantity, price))
        conn.commit()
        conn.close()
        
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('produto_form.html', action="Cadastrar", is_admin=is_admin())

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    produto = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    
    if not produto:
        conn.close()
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Nome é um campo obrigatório.', 'danger')
            return redirect(url_for('editar_produto', id=id))
            
        try:
            quantity = int(request.form.get('quantity'))
            min_quantity = int(request.form.get('min_quantity'))
            price = float(request.form.get('price'))
        except (ValueError, TypeError):
            flash('Quantidade, Quantidade Mínima e Preço devem ser preenchidos e ser números.', 'danger')
            return redirect(url_for('editar_produto', id=id))
            
        conn.execute('''
            UPDATE products 
            SET name = ?, description = ?, quantity = ?, min_quantity = ?, price = ?
            WHERE id = ?
        ''', (name, description, quantity, min_quantity, price, id))
        conn.commit()
        conn.close()
        
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
        
    conn.close()
    return render_template('produto_form.html', action="Editar", produto=produto, is_admin=is_admin())

@app.route('/usuarios/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if not is_admin():
        flash('Acesso negado. Apenas administradores podem cadastrar novos usuários.', 'danger')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if not username or not password or not role:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('cadastrar_usuario'))
            
        hashed_pw = generate_password_hash(password)
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                         (username, hashed_pw, role))
            conn.commit()
            flash('Usuário cadastrado com sucesso!', 'success')
            conn.close()
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('cadastrar_usuario'))
            
    return render_template('usuario_form.html', is_admin=is_admin())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
