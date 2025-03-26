from flask import Blueprint, render_template
from models.user import User
from flask_login import login_required
from db import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
