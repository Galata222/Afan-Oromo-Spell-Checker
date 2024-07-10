import string
import json
import os

verbClasses = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10']
nounClasses = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
              'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']


class KnowledgeBase:
    def __init__(self, dictionary_file_path, affix_file_path):
        self.dictionary_file_path = dictionary_file_path
        self.affix_file_path = affix_file_path
        self.words = {}
        self.affixes = {}
        self.custom_dictionary = set()  # Custom dictionary
        self.ignored_words = set()  # Ignore list
        self.load_knowledge_base()
        self.loadLocalStorage()

    def load_knowledge_base(self):
        with open(self.affix_file_path, 'r') as f:
            for line in f:
                values = line.strip().split()

                if len(values) == 5:
                    option_name, flag, stripping, affix, condition = values
                    if flag not in self.affixes:
                        self.affixes[flag] = []
                    self.affixes[flag].append({
                        'option_name': option_name,
                        'flag': flag,
                        'stripping': stripping,
                        'affix': affix,
                        'condition': condition
                    })
                    # print(f"Added affix {affix} to class {flag}")

        with open(self.dictionary_file_path, 'r') as f:
            for line in f:
                if '/' in line:
                    rootWord, affix_classes = line.strip().split('/')
                    self.words[rootWord] = [affix['affix'] for affix_class in affix_classes.split(
                        ',') for affix in self.affixes.get(affix_class, [])]
                    # print(f"Added word with affixes {self.words[rootWord]}")

                else:
                    rootWord = line.strip()
                    self.words[rootWord] = []
                    # print(f"Added word {rootWord} with no affixes")

    def loadLocalStorage(self):
        try:
            with open('custom_dictionary.json', 'r') as file:
                data = json.load(file)
                self.custom_dictionary = set(data['custom_dictionary'])
                # print(f"Loaded custom dictionary: {self.custom_dictionary}")
        except FileNotFoundError:
            print("No custom dictionary found")

        try:
            with open('ignored_words.json', 'r') as file:
                data = json.load(file)
                self.ignored_words = set(data['ignored_words'])
                # print(f"Loaded ignored words: {self.ignored_words}")
        except FileNotFoundError:
            print("No ignored words found")

    def saveLocalStorage(self):
        data_custom = {'custom_dictionary': list(self.custom_dictionary)}
        with open('custom_dictionary.json', 'w') as file:
            json.dump(data_custom, file)
            # print(f"Saved custom dictionary: {self.custom_dictionary}")

        data_ignored = {'ignored_words': list(self.ignored_words)}
        with open('ignored_words.json', 'w') as file:
            json.dump(data_ignored, file)
            # print(f"Saved ignored words: {self.ignored_words}")

    def is_valid_word(self, rootWord):
        rootWord = rootWord.lower()
        punctuation = string.punctuation.replace("'", "").replace("-", "")
        # Remove punctuation from the rootWord
        rootWord_without_punctuation = rootWord.translate(
            str.maketrans('', '', punctuation))
        # print(f"rootWord_without_punctuation is {rootWord_without_punctuation}")
        rootWord_filtered = rootWord_without_punctuation
        # print(f"Converted rootword from capital to small is {rootWord_filtered}")
        # Check if the rootWord without punctuation is in the words or custom_dictionary
        is_valid = any(
            rootWord_filtered == word.lower() or rootWord_filtered in affixes
            for word, affixes in self.words.items()
        ) or rootWord_filtered in self.custom_dictionary or rootWord_filtered in self.ignored_words
        # print(f"Word {rootWord_filtered} is valid: {is_valid}")
        return is_valid

    def add_to_custom_dictionary(self, word):
        # print(f"Adding {word} to custom dictionary...")
        self.custom_dictionary.add(word)
        self.saveLocalStorage()

    def ignore_word(self, word):
        # print(f"Ignoring word {word}...")
        self.ignored_words.add(word)
        self.saveLocalStorage()

    def get_affixes_for_root(self, rootWord):
        affixes = self.words.get(rootWord, [])
        # print(f"Affixes for {rootWord}: {affixes}")
        return affixes

    def find_valid_root_for_affix(self, affix):
        valid_roots = []
        for root, affixes in self.words.items():
            if affix in affixes:
                valid_roots.append(root)
        # print(f"Valid roots for {affix}: {valid_roots}")
        return valid_roots
    def get_affixes(self):
        return self.affixes
    def get_roots(self):
        return self.words   
    def morphological_analysis(self, word):
        word = word.lower()
        # if word.isdigit():
        #     return True
        # print(f"word:{word}")
        if word in self.ignored_words:
            return {word: []}, {}  # Change the output structure to use lists instead of sets

        morphological_dict = {}
        for affix_class, rules in self.affixes.items():
            for rule in rules:
               if word.endswith(rule.get('affix')) and rule['flag'] in nounClasses:
                    if rule['stripping'] != '0':
                        stripped_letter = rule['stripping']
                        root = word[:len(word) - len(rule['affix'])
                                    ] + stripped_letter
                        # print(f"rootsss:{root}")
                        morphological_dict[root] = set()
                        morphological_dict[root].add(rule['affix'])
                        for root, affixes in morphological_dict.items():
                            morphological_dict[root] = list(affixes)

        for affix_class, rules in self.affixes.items():
            for rule in rules:
                if word.endswith(rule.get('affix')):
                    root = word[:len(word) - len(rule['affix'])]
                    if root not in morphological_dict:
                        morphological_dict[root] = set()
                    morphological_dict[root].add(rule['affix'])
                else:
                    continue  # Go to the next rule if no affix is found

        # If no affix is found, add roots directly from self.words
        for root in self.words.keys():
            if word.startswith(root):
                affix = word[len(root)-len(word):]
                # if root not in morphological_dict:
                morphological_dict[root] = set()
                morphological_dict[root].add(affix)

        # Convert sets to lists
        for root, affixes in morphological_dict.items():
            morphological_dict[root] = list(affixes)
            # For striping Noun classes 

            # else:
                
            #     root = word[:len(word) - len(rule['affix'])]

            # roots.append(root)
            # affixes.append(rule['affix'])
        print("morphological dictionary:", morphological_dict)
        return morphological_dict, {}  # Return empty dict for affixes

    # def morphological_analysis(self, word):
    #     word = word.lower()
    #     print(f"word:{word}")
    #     if word in self.ignored_words:
    #     # print(f"Word {word} is ignored")
    #         return {word}, set()  # Change lists to sets

    #     roots = set()
    #     affixes = set()
    #     for affix_class, rules in self.words.items():
    #         for rule in rules:
    #             if word.endswith(rule['affix']):
    #                 root = word[:len(word) - len(rule['affix'])]
    #                 roots.add(root)
    #                 affixes.add(rule['affix'])

    #     print("roots:", roots, "affixes:", affixes)
        # for affix_class, rules in self.affixes.items():

        #     for rule in rules:

        #         if word.endswith(rule['affix']) and rule['flag'] in verbClasses:

        #             if rule['stripping'] != '0':
        #                 stripped_letter = rule['stripping']
        #                 root = word[:len(word) - len(rule['affix'])
        #                             ] + stripped_letter
        #                 roots.append(root)
        #                 affixes.append(rule['affix'])
        #             else:
        #                 root = word[:len(word) - len(rule['affix'])]
        #             roots.append(root)
        #             affixes.append(rule['affix'])
        #             # print(f"rule of condtion:{rule['condition']}")

        #         elif word.endswith(rule['affix']) and rule['flag'] in nounClasses:
        #             if rule['stripping'] != '0':
        #                 stripped_letter = rule['stripping']
        #                 root = word[:len(word) - len(rule['affix'])
        #                             ] + stripped_letter
        #                 # print(f"rootsss:{root}")
        #                 roots.append(root)
        #                 affixes.append(rule['affix'])
        #             else:
        #                 root = word[:len(word) - len(rule['affix'])]

        #             roots.append(root)
        #             affixes.append(rule['affix'])
        #     # print("roots: ", roots, "affixes: ", affixes, "classes: ", rule['flags'])
        # for affix_class, rules in self.affixes.items():
        #     for rule in rules:
        #         if word.startswith(rule['affix']) and rule['option_name'] == 'PFX':
        #             if rule['stripping'] != '0':
        #                 stripped_letter = rule['stripping']
        #                 root = word[len(rule['affix']):]

        #             else:
        #                 root = word[len(rule['affix']):]

        #             roots.append(root)
        #             affixes.append(rule['affix'])

        # valid_roots = []
        # valid_affixes = []

        # for root, affix in zip(roots, affixes):
        #     if self.is_valid_word(root) and affix in self.get_affixes_for_root(root):
        #         valid_roots.append(root)
        #         valid_affixes.append(affix)
        # # print("valid_roots: ", valid_affixes, "valid_affixes", valid_affixes)
        # return valid_roots, valid_affixes

    def get_affix_class_for_root(self, word):
        affix_class = None
        with open(self.dictionary_file_path, 'r') as f:
            for line in f:
                if '/' in line:
                    rootWord, affix_classes = line.strip().split('/')
                    if (rootWord == word):
                        affix_class = affix_classes
        return affix_class
