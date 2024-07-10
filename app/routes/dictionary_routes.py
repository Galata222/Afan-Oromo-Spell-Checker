# app.py

from flask import Flask, render_template, request, jsonify, Blueprint

app = Flask(__name__)

dictionary_routes = Blueprint('dictionary_routes', __name__)

@dictionary_routes.route('/add_to_dictionary', methods=['GET'])
def index():
    return render_template('dictionary.html')

@dictionary_routes.route('/add_to_dictionary', methods=['POST'])
def check_word():
    data = request.get_json()
    root_word = data['rootWord']
    class_word = data['classWord']
    dictionary_path = 'app/knowledge_base/resources/dictionary.dic'

    with open(dictionary_path, 'r') as f:
        dictionary = f.read().splitlines()

    if class_word == 'Verb':
        verb_stem, verb_class = classify_verb(root_word)
        verb_stem = verb_stem.lower()
        mergedWord = verb_stem + '/' + verb_class
    elif class_word == "Noun":
        noun_stem, noun_class = classify_noun(root_word)
        noun_stem = noun_stem.lower()
        mergedWord = noun_stem + '/' + noun_class
    else:
        root_word = root_word.lower()
        mergedWord = root_word

    if mergedWord not in dictionary:
        with open(dictionary_path, 'a') as f:
            f.write(mergedWord + '\n')

        # Read the dictionary again, sort it, and overwrite the file
        with open(dictionary_path, 'r') as f:
            lines = f.readlines()
            lines.sort()

        with open(dictionary_path, 'w') as f:
            f.writelines(lines)

        return jsonify({'exists': False})
    else:
        return jsonify({'exists': True})

def classify_verb(stem):
    if stem[-1] not in 'aeiou':
        # Verb
        # Rule for classifying verbs
        if stem.endswith(('f', 'k', 'm', 'n')):
            return stem, 'V1'
        elif stem.endswith("'") or stem.endswith(("dh", "h")):
            return stem, 'V2'
        elif stem.endswith(('b', 'd', 'g')):
            return stem, 'V3'
        elif stem.endswith('t'):
            return stem, 'V4'
        elif stem.endswith(('s', 'ch', 'c')):
            return stem, 'V5'
        elif stem.endswith('l'):
            return stem, 'V6'
        elif stem.endswith('r'):
            return stem, 'V7'
        elif stem.endswith(('x', 'q', 'ph')):
            return stem, 'V8'
        elif stem.endswith('aaw'):
            return stem, 'V9'
        elif stem.endswith('j'):
            return stem, 'V10'
        else:
            return stem, ''
    else:
        return stem, ''

def classify_noun(stem):
    if stem[0].isupper():
        return stem, 'N7'
    elif stem.endswith(('aa', 'ee', 'oo', 'uu', 'ii')):
        return stem, 'N1'
    elif stem.endswith(('a', 'e', 'o', 'u', 'i')) and stem[-3:-2] in 'aa ee oo uu ii' and stem[-2] in 'lrm':
            return stem, 'N2'
    elif stem.endswith(('eessa', 'eettii', 'eecha', 'eeysa', 'eeytii')):
        return stem, 'N4'
    elif stem.endswith(('a', 'e', 'o', 'u', 'i')) and stem[-2] in 'bdgn':
        return stem, 'N3'
    elif stem[-1] in 'bcdfghjklmnpqrstvwxyz':
        return stem, 'N5'
    else:
        return stem, 'N6'
