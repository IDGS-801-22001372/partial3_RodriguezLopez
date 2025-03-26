class Config(object):
    SECRET_KEY = 'Clave Nueva'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Deadmau6@localhost/examen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
