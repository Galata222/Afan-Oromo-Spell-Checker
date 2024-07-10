from flask import jsonify, Blueprint, request
from app.error_detection.error_detection import ErrorDetection
from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer

error_detection_routes = Blueprint('error_detection_routes', __name__)

@error_detection_routes.route('/detect_errors', methods=['POST'])
def detect_errors():
    data = request.get_json()
    tokens = data.get('tokens', [])
    
    kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')
    ma = MorphologicalAnalyzer(kb)
    error_detection = ErrorDetection(kb, ma)
    
    errors = {}
    error_classes = {}
    for token in tokens:
        is_error, error_class = error_detection.is_valid_word(token)
        errors[token] = is_error
        if not is_error: 
            error_classes[token] = error_class
    print("error_classes:",error_classes)
    return jsonify({'errors': errors, "error_classes": error_classes})
def get_error_class():
    data = request.get_json()
    tokens = data.get('tokens', [])
    
    kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')
    ma = MorphologicalAnalyzer(kb)
    error_detection = ErrorDetection(kb, ma)
    errors = {}
    for token in tokens:
        is_error, error_class = error_detection.is_valid_word(token)
        if not is_error:
            errors[token] = is_error

    print("List of Errors to be corrected:",errors)
    return  errors 



   
