from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '1234567890'

register_admin_routes = Blueprint('register_admin_routes', __name__)
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rooot'
app.config['MYSQL_DB'] = 'oasc_db'

mysql = MySQL(app)

@register_admin_routes.route('/register_admin', methods=['GET'])
def index():
    return render_template('register_admin.html')

@register_admin_routes.route('/register_admin', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, email, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (username, password, email, first_name, last_name, phone_number))
        mysql.connection.commit()
        cur.close()

        flash('You have successfully registered', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('register_admin.html')

if __name__ == '__main__':
    app.run(debug=True)
