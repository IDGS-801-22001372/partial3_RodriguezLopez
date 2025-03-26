from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, validators
from wtforms import EmailField
from wtforms import validators
from wtforms import Form, IntegerField, StringField, EmailField, validators
 
class ProveedorForm(FlaskForm):  
    nombre = StringField('nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4, max=50, message='Requiere min=4, max=50')
    ])
    empresa = StringField('teléfono', [
        validators.DataRequired(message='Empresa es requerido'),
        validators.length(min=4, max=100, message='Requiere min=10, max=15')
    ])
    correo = EmailField('correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Ingrese un correo válido')
    ])