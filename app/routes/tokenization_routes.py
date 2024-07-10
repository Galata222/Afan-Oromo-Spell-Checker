# app/routes/tokenization_routes.py
from flask import jsonify, Blueprint, request
from app.tokenizer.tokenizer import tokenize

tokenization_routes = Blueprint('tokenization_routes', __name__)

@tokenization_routes.route('/tokenize', methods=['POST'])
def tokenize_text():
    data = request.get_json()
    text = data.get('text', '')
    tokens = tokenize(text)
    return jsonify({'tokens': tokens})
