from flask import  request, jsonify,Blueprint,render_template

footer_routes = Blueprint('footer_routes',__name__)

@footer_routes.route('/footer')
def about():
    return render_template('footer.html',)