from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_url, LoginManager, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

# Configuración
class Config(object):
    SECRET_KEY = 'Clave Nueva'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Deadmau6@localhost/examen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Cargar la configuración antes de inicializar db
    app.config.from_object(DevelopmentConfig)

    # Inicializar las extensiones
    db.init_app(app)
    bcrypt = Bcrypt(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "danger"


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Modelos
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), nullable=False, unique=True)
        password = db.Column(db.String(100), nullable=False)
        
    # Formularios
    class RegisterForm(FlaskForm):
        username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
        password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
        submit = SubmitField("Register")

        def validar_usuario(self, username):
            usuario_existente = User.query.filter_by(username=username.data).first()
            if usuario_existente:
                raise ValidationError("Ese usuario ya existe")
    
    class LoginForm(FlaskForm):
        username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
        password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
        submit = SubmitField("Login")

    # Crear las tablas en la base de datos
    with app.app_context():
        db.create_all()

    # Definir las rutas
    @app.route('/')
    def index():
        return render_template('index.html')

    # Log In
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    flash('Datos incorrectos', 'danger')
            else:
                flash('Usuario no encontrado', 'danger')
                    
        return render_template('login.html', form=form)
    
    #Pagina principal
    @app.route('/dashboard', methods=['GET', 'POST'])
    @login_required
    def dashboard():
        return render_template('dashboard.html')
    
    #Pagina principal
    @app.route('/usuarios', methods=['GET', 'POST'])
    @login_required
    def usuarios():
        users = User.query.all()
        return render_template('usuarios.html', users=users)
    
    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))


    #Registro
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)