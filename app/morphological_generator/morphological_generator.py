
from app.knowledge_base.knowledge_base import KnowledgeBase
from app.knowledge_base.knowledge_base import  nounClasses
from app.error_correction.error_correction import ErrorCorrection
class MorphologicalGenerator:
    def __init__(self, knowledge_base: KnowledgeBase,):
        self.knowledge_base = knowledge_base

    def generate_words(self, input_morphemes):
        correct_words = []

        for morpheme in input_morphemes:
           
            if self.knowledge_base.is_valid_word(morpheme):  # If the morpheme is a valid root
                word_forms = self.generate_word_forms_from_root(morpheme)
            else:  # If the morpheme is an affix
                word_forms = self.generate_word_forms_from_affix(morpheme)
            correct_words.extend(word_forms)

        return correct_words

    def generate_word_forms_from_root(self, root):
        word_forms = []

        # Case 1: Root word with no affix
        affixClass= self.knowledge_base.get_affix_class_for_root(root)
        if self.knowledge_base.is_valid_word(root) and affixClass in nounClasses :
            word_forms.append(root)

        # Case 2: Root word with affixes
        affixes = self.knowledge_base.get_affixes_for_root(root)
        if affixes:
            for affix in affixes:
                word_form = root + affix
                word_forms.append(word_form)

        return word_forms

    def generate_word_forms_from_affix(self, affix):
        word_forms = []
        roots = self.knowledge_base.find_valid_root_for_affix(affix)

        for root in roots:
            word_form = root + affix
            word_forms.append(word_form)

        return word_forms
    

    
