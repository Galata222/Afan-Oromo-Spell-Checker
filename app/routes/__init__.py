# app/routes/__init__.py
from flask import Blueprint

tokenization_routes = Blueprint('tokenization_routes', __name__)

from . import tokenization_routes  # Import the route definitions
