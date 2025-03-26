from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from forms.user_form import RegisterForm
from db import db
from flask_login import login_required
from flask_bcrypt import Bcrypt
import json

usuarios_bp = Blueprint('usuarios', __name__)
bcrypt = Bcrypt()

@usuarios_bp.route('/usuarios')
@login_required
def usuarios():
    users = User.query.all()
    return render_template('usuarios/usuarios.html', users=users)

# Registro
@usuarios_bp.route('/agregar', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('usuarios.usuarios'))
    
    return render_template('usuarios/agregar_usuarios.html', form=form)

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuarios(id):
    user = User.query.get_or_404(id)
    form = RegisterForm(obj=user)
    
    if request.method == 'POST' and form.validate():
        user.username = form.username.data
        if form.password.data:  # Solo actualizar si se ingresa una nueva contraseña
            user.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios.usuarios'))  # Redirección corregida

    return render_template('usuarios/editar_usuarios.html', form=form, user=user)





