from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm  
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Defina uma chave secreta para usar o flash (Opcional)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Modelo de usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('inicio'))  
        else:
            flash('Nome de usuário ou senha incorretos. Tente novamente.', 'error')
    return render_template('login.html')

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login agora.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

# Rota da página inicial 1
@app.route('/')  
def home():
    return render_template('home.html')

# Rota da página inicial 2
@app.route('/inicio')  
def inicio():  
    username = session.get('username') 
    return render_template('inicio.html', username=username)  

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout bem-sucedido!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
