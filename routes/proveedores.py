from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.proveedores import Proveedores
from forms.proveedores_form import ProveedorForm
from db import db

from flask_login import login_required

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/proveedores')
@login_required
def proveedores():
    proveedores = Proveedores.query.all()
    return render_template('/proveedores/proveedores.html', proveedores=proveedores)

@proveedores_bp.route('/proveedores/agregar', methods=['GET', 'POST'])
@login_required
def agregar_proveedor():
    form = ProveedorForm(request.form)
    if request.method == 'POST' and form.validate():
        proveedor = Proveedores(
            nombre=form.nombre.data,
            empresa=form.empresa.data,
            correo=form.correo.data
        )
        db.session.add(proveedor)
        db.session.commit()
        flash('Proveedor agregado correctamente', 'success')
        return redirect(url_for('proveedores.proveedores'))
    return render_template('proveedores/agregar_proveedor.html', form=form)

@proveedores_bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedores.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)
    
    if request.method == 'POST' and form.validate():
        proveedor.nombre = form.nombre.data
        proveedor.empresa = form.empresa.data
        proveedor.correo = form.correo.data
        db.session.commit()
        flash('Proveedor actualizado correctamente', 'success')
        return redirect(url_for('proveedores.proveedores'))

    return render_template('proveedores/editar_proveedor.html', form=form, proveedor=proveedor)




