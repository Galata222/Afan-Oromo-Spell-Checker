from flask import  request, jsonify,Blueprint
from app.knowledge_base.knowledge_base import KnowledgeBase

custom_dictionary_routes = Blueprint('custom_dictionary_routes', __name__)
kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')

@custom_dictionary_routes.route('/add_to_custom_dictionary', methods=['POST'])
def add_to_ignored_words():
    data = request.get_json()
    # print(f"data from custom dictionary:{data}")
    word = data.get('word',[])
    # print(f"data from custom dictionary:{word}")
    if word:
        kb.add_to_custom_dictionary(word)
        return jsonify({'message': f'Added {word} to custom dictionary words.'}), 200
    else:
        return jsonify({'message': 'No word provided.'}), 400
