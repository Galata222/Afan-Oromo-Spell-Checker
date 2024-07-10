from flask import  request, jsonify,Blueprint
from app.knowledge_base.knowledge_base import KnowledgeBase

ignored_word_routes = Blueprint('ignored_word_routes', __name__)
kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')

@ignored_word_routes.route('/add_to_ignored_words', methods=['POST'])
def add_to_ignored_words():
    data = request.get_json()
    # print(f"data from ingored:{data}")
    word = data.get('word',[])
    # print(f"word from ingored:{word}")
    if word:
        kb.ignore_word(word)
        return jsonify({'message': f'Added {word} to ignored words.'}), 200
    else:
        return jsonify({'message': 'No word provided.'}), 400
