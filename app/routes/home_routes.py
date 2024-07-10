# app/routes/home_routes.py
from flask import Blueprint, render_template

index_app = Blueprint('index_app', __name__)

@index_app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')
