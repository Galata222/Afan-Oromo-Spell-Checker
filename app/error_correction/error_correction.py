import re
import Levenshtein
from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer
from app.error_detection.error_detection import ErrorDetection
from app.routes.error_detection_routes import get_error_class

class ErrorCorrection:
    def __init__(self, knowledge_base: KnowledgeBase, morphological_analyzer: MorphologicalAnalyzer, aff_file_path):
        self.knowledge_base = knowledge_base
        self.morphological_analyzer = morphological_analyzer
        self.replacement_rules = self.load_replacement_rules(aff_file_path)
        

    def load_replacement_rules(self, aff_file_path):
        replacement_rules = {}
        with open(aff_file_path, 'r') as f:
            for line in f:
                if line.startswith('REP'):
                    _, rule, replacement = line.strip().split()
                    replacement_rules[rule] = replacement
        return replacement_rules

    def apply_replacement_rules(self, error):
        if isinstance(error, dict):
            corrected_error = {k: self.apply_replacement_rules(v) for k, v in error.items()}
        elif isinstance(error, str):
            for rule, replacement in self.replacement_rules.items():
                error = error.replace(rule, replacement)
            corrected_error = error
        else:
            raise ValueError("Expected a string or dict for argument 'error'")
        return corrected_error
    def correct_by_levensthein(self):
        get_error_class()
    def custom_levenshtein(self, s1, s2):
        # Initialize substitution, insertion, and deletion costs
        substitution_cost = 1
        insertion_cost = 1
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

    def correct_error(self, error):
        # Apply the replacement rules to the error
        corrected_error = self.apply_replacement_rules(error)

        # Get all valid words from the knowledge base
        valid_words = self.knowledge_base.words.keys()

        # Find the valid words that have the minimum Levenshtein distance
        min_distance = float('inf')
        closest_words = []
        word_distances = {}

        for valid_word in valid_words:
            distance = self.custom_levenshtein(valid_word, corrected_error)
            word_distances[valid_word] = distance

            if distance < min_distance:
                min_distance = distance
                closest_words = [valid_word]
            elif distance == min_distance:
                closest_words.append(valid_word)

        # Sort closest_words based on their Levenshtein distance to corrected_error
        closest_words.sort(key=word_distances.get)

        # Analyze the morphemes of the corrected error
        valid_roots, valid_affixes = self.morphological_analyzer.analyze(corrected_error)

        # Check if roots are valid and affixes are not, return valid roots
        if valid_roots and not valid_affixes:
            return valid_roots

        # Check if affixes are valid and roots are not, return valid affixes
        elif not valid_roots and valid_affixes:
            return valid_affixes

        # If both roots and affixes are valid, you may want to decide which one to prioritize
        # For now, returning closest words if both roots and affixes are valid
        else:
            return closest_words
