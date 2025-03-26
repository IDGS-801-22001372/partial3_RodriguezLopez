from flask import Flask
from config import DevelopmentConfig
from db import db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from routes.auth import auth
from routes.main import main
from routes.usuarios import usuarios_bp
from routes.venta import ventas_bp
from routes.proveedores import proveedores_bp
from models.user import User

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(DevelopmentConfig)

    # Inicialización de extensiones
    db.init_app(app)
    bcrypt = Bcrypt(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registra los Blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(proveedores_bp)
    app.register_blueprint(usuarios_bp)


    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
