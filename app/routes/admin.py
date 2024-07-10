from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

app = Flask(__name__)

# Define admin blueprint
admin_routes = Blueprint('admin_routes', __name__)

# Define routes


@admin_routes.route('/admin')
def admin():
    return render_template('admin.html')

# @app.route('/admin/user_management')
def user_management():
    return render_template() # Specify the template name


