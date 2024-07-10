N = 3  # Set your desired value for N


class SuggestionRanking:
    qwerty_layout = {
        'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4),
        'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
        'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4),
        'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8), ';': (1, 9),
        'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4),
        'n': (2, 5), 'm': (2, 6), ',': (2, 7), '.': (2, 8)
    }

    def __init__(self, aff_file_path):
        self.replacement_rules = self.load_replacement_rules(aff_file_path)

    def load_replacement_rules(self, aff_file_path):
        replacement_rules = {}
        with open(aff_file_path, 'r') as f:
            for line in f:
                if line.startswith('REP'):
                    _, rule, replacement = line.strip().split()
                    replacement_rules[rule] = replacement
        return replacement_rules

    def rank_suggestions(self, suggestions, misspelled_word):
        if not suggestions:
            return []

        top_ranked_suggestions = [
            (suggestion, 1) if self.is_replacement_rule(suggestion, misspelled_word) else
            (suggestion, (self.calculate_levenshtein_distance(suggestion, misspelled_word),
                          self.calculate_character_distance(suggestion, misspelled_word)))
            for suggestion in suggestions
        ]

        top_ranked_suggestions.sort(key=lambda x: x[1])

        n = min(len(top_ranked_suggestions), N)
        return [word for word, _ in top_ranked_suggestions[:n]]

    def is_replacement_rule(self, suggestion, misspelled_word):
        return any(rule in misspelled_word for rule in suggestion.split("_"))

    def calculate_levenshtein_distance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i]
                                       [j - 1], dp[i - 1][j - 1])

        return dp[m][n]

    def calculate_character_distance(self, word1, word2):
        distance = 0
        for char1, char2 in zip(word1, word2):
            if char1 in self.qwerty_layout and char2 in self.qwerty_layout:
                distance += ((self.qwerty_layout[char1][0] - self.qwerty_layout[char2][0]) ** 2 +
                             (self.qwerty_layout[char1][1] - self.qwerty_layout[char2][1]) ** 2) ** 0.5
        return distance
