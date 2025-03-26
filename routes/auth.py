from flask import Blueprint, render_template, redirect, url_for, flash
from db import db
from models.user import User
from forms.user_form import RegisterForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

# Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Datos incorrectos', 'danger')
    
    return render_template('login.html', form=form)

# Logout
@auth.route('/logout')
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))
