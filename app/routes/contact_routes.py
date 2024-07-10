from flask import  request, jsonify,Blueprint,render_template

contact_routes = Blueprint('contact_routes',__name__)

@contact_routes.route('/contact')
def about():
    return render_template('contact.html',)