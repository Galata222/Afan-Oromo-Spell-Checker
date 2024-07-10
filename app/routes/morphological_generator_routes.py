from flask import jsonify, Blueprint, request
from app.morphological_generator.morphological_generator import MorphologicalGenerator
from app.knowledge_base.knowledge_base import KnowledgeBase, verbClasses,nounClasses
import Levenshtein

morphological_generator_routes = Blueprint('morphological_generator_routes', __name__)

@morphological_generator_routes.route('/generate_words', methods=['POST'])
def generate_words():
    data = request.get_json()
    corrections = data.get('morphemes', [])
    user_input_root = data.get('error_class', [])
    # misspelled_word = data.get('errors', "")

    kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')
    morphological_generator = MorphologicalGenerator(kb)
    # print('Wordssssss ', str(for key in corrections.keys()) )
    words = []
    if not corrections:
        with open('app/knowledge_base/resources/dictionary.dic', 'r') as f:
            for line in f:
                if '/' in line:
                    rootWord, affix_classes = line.strip().split('/')
                    distance = Levenshtein.distance(user_input_root, rootWord)
                    if distance < 3 and affix_classes not in verbClasses:
                        words.append(rootWord)
            
    for root in corrections.keys():
        with open('app/knowledge_base/resources/dictionary.dic', 'r') as f:
            for line in f:
                if '/' in line:
                    rootWord, affix_classes = line.strip().split('/')
                    affix_of_kb = kb.get_affixes()
                    affixes_of_root =kb.get_roots()
                    if rootWord == root:
                        
                        for affix_class, rules in affix_of_kb.items():
                            for rule in rules:
                                # if rule['stripping'] != '0':
                                if affix_classes == rule['flag'] :
                                    # print("Testsssssssss flaggsss", rule['flag'])
                                    if rule['stripping'] != '0':
                                        stripped_letter = rule['stripping']
                                        # print("Testsssssssss", stripped_letter)
                                        stripped_root = root[:len(root)-len(stripped_letter)] 
                                        for affixes in corrections.values():
                                            for affix in affixes:
                                                if affix in affixes_of_root[root]:
                                                    word = str(stripped_root) + str(affix)
                                                    if word not in words:
                                                        words.append(word)

        for affixes in corrections.values():
            for affix in affixes:
                word = str(root) + str(affix)
                if word not in words:
                    words.append(word)
    print('Wordssssss ', words)

    return jsonify({'words': words})
