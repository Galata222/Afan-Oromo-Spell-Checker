# app/__init__.py
from flask import Flask
from app.routes.tokenization_routes import tokenization_routes
from app.routes.home_routes import index_app
from app.routes.error_detection_routes import error_detection_routes
from app.routes.error_correction_routes import error_correction_routes
from app.routes.morphological_generator_routes import morphological_generator_routes
from app.routes.suggestion_routes import suggestion_ranking_routes
from app.routes.ignored_word_routes import ignored_word_routes
from app.routes.custom_dictionary_routes import custom_dictionary_routes
from app.routes.about_routes import about_routes
from app.routes. contact_routes import contact_routes
from app.routes.footer_routes import footer_routes
from app.routes.dictionary_routes import dictionary_routes
from app.routes.login import login_routes  # Import login_routes Blueprint
from app.routes.admin import admin_routes  # Import login_routes Blueprintadmin_register_routes
from app.routes.register_admin import register_admin_routes
def create_app():
    app = Flask(__name__, static_url_path='/static')
    # Set the secret key
    app.config['SECRET_KEY'] = '1234567890'
    app.register_blueprint(tokenization_routes, url_prefix='/')
    app.register_blueprint(index_app, url_prefix='/')
    app.register_blueprint(error_detection_routes, url_prefix='/')
    app.register_blueprint(error_correction_routes,url_prefix='/')
    app.register_blueprint(morphological_generator_routes,url_prefix='/')
    app.register_blueprint(suggestion_ranking_routes,url_prefix='/')
    app.register_blueprint(ignored_word_routes,url_prefix='/')
    app.register_blueprint(custom_dictionary_routes,url_prefix='/')
    app.register_blueprint(about_routes,url_prefix='/')
    app.register_blueprint(contact_routes,url_prefix='/')
    app.register_blueprint(footer_routes,url_prefix='/')
    app.register_blueprint(dictionary_routes,url_prefix='')
    app.register_blueprint(admin_routes,url_prefix='/')
    app.register_blueprint(login_routes,url_prefix='/')  # Register login_routes with a prefix
    app.register_blueprint(register_admin_routes,url_prefix='/')

    return app