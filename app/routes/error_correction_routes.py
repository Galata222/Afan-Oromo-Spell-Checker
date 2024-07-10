from flask import jsonify, Blueprint, request
from app.error_correction.error_correction import ErrorCorrection
from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer
import Levenshtein
error_correction_routes = Blueprint('error_correction_routes', __name__)

@error_correction_routes.route('/correct_errors', methods=['POST'])
def correct_errors():
    data = request.get_json()

    error_class = data.get('error_class', []) # the error class contains token of user input
    details = data.get('details', []) #contains dictionary of of error class which is root as key and affixes as values
    # print("Error calsssssss", error_class)
    # print("details calsssssss", details)
    # print(f"Errors from error detection: {errors}")
    kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')
    ma = MorphologicalAnalyzer(kb)
    error_correction = ErrorCorrection(kb, ma, 'app/knowledge_base/resources/dictionary.aff')  # Pass the .aff file path to ErrorCorrection
    corrections = {}
    List_of_corrections=[]
    for element in details:
        # print("Error calsssssss", error_classes)
        # print("Error calsssssss", error_classes)
        affixes = kb.get_roots()
        if element in affixes:
            affixes_of_root = affixes[element]
            affix_of_element = details[element]
            # print("aaffffix", affix_of_element)
            for affix in affixes_of_root:
            # print("Error calssssss", affixes_of_root)
                distance = Levenshtein.distance(affix_of_element, affix)
                if distance < 3:
                    List_of_corrections.append(affix)
                    corrections[element]=List_of_corrections
        list_of_affixes = kb.get_affixes()
        List_of_corrections.append(details[element])
        for rules in list_of_affixes.values():
            for rule in rules:
                if details[element] == rule['affix']:
                    flag = rule['flag']
                    
                    # print("flaggggggg",flag)
                    with open('app/knowledge_base/resources/dictionary.dic', 'r') as f:
                        for line in f:
                            if '/' in line:
                                rootWord, affix_classes = line.strip().split('/')
                                if flag == affix_classes:
                                    # print("flaggggggg",element)
                                    distance = Levenshtein.distance(element, rootWord)
                                    if distance < 3:
                                        print("elelmenttt ",rootWord)
                                        
                                        corrections[rootWord]=List_of_corrections
            
                    # print(f"Added word with affixes {self.words[rootWord]}")

                    
                        # corrections[element]=List_of_corrections

    print("lissttttttt", corrections)                

        # correction = error_correction.correct_error(element) 
        # print(f"correction from error correction routes: {correction}")
        # corrections.update(correction)

    return jsonify({'corrections': corrections})
def custom_levenshtein(s1, s2):
        # Initialize substitution, insertion, and deletion costs
        substitution_cost = 1
        insertion_cost = 2
        deletion_cost = 1

        # Initialize the matrix with dimensions (m+1) x (n+1)
        m = len(s1)
        n = len(s2)
        matrix = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill in the first row and column of the matrix
        for i in range(m + 1):
            matrix[i][0] = i
        for j in range(n + 1):
            matrix[0][j] = j

        # Compute minimum edit distance using dynamic programming
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else substitution_cost
                matrix[i][j] = min(matrix[i - 1][j] + deletion_cost,       # Deletion
                                   matrix[i][j - 1] + insertion_cost,      # Insertion
                                   matrix[i - 1][j - 1] + cost)            # Substitution

        # Return the minimum edit distance between the two strings
        return matrix[m][n]