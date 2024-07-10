from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer
from app.knowledge_base.knowledge_base import nounClasses,verbClasses
class ErrorDetection:
    def __init__(self, knowledge_base: KnowledgeBase, morphological_analyzer: MorphologicalAnalyzer):
        self.knowledge_base = knowledge_base
        self.morphological_analyzer = morphological_analyzer
      
    def is_valid_word(self, word):
        v_root_i_affix ={}
        i_root_v_affix ={}
        i_root_i_affix ={}
        # Check if the word itself is valid
        if self.knowledge_base.is_valid_word(word):
            affixClass = self.knowledge_base.get_affix_class_for_root(word)
            if affixClass not in verbClasses:
                return True, {}
        
        # Analyze the word morphologically
        morphological_dictionary, _ = self.morphological_analyzer.analyze(word)
        affix_rules = self.knowledge_base.get_affixes()
        root_affixes = self.knowledge_base.get_roots()
        # print("root_affixes", morphological_dictionary.keys())
        # Iterate through roots in the morphological dictionary

        for root in morphological_dictionary.keys():
                # Check if the root is in the dictionary
            affix_of_root = morphological_dictionary[root][0]
            if self.knowledge_base.is_valid_word(root):
                
                # print("roots", root)
                # print("affix_of_root", affix_of_root)
                        # Check if the affix of the root matches any known affix rules
                if any(affix_of_root == affix['affix'] for affixes in affix_rules.values() for affix in affixes):
                    affix_list = root_affixes.get(root, [])
                            # Check if the affix of the root matches any known affixes associated with the root
                    if any(affix_of_root == affix for affix in affix_list):
                        return True,{}
                else:
                    v_root_i_affix[root]=affix_of_root
                    # print("v_root_i_affix",v_root_i_affix)
                    return False, v_root_i_affix     
            else:
                i_root_v_affix [root]=affix_of_root
        return False, i_root_v_affix
        
                # else:
                #     for affixes in affix_rules.items():
                #         for affix in affixes:
                #             affix_of_root  = morphological_dictionary[root][0]
                #             if affix_of_root == affix['affixes']:
                #                 affix_list = root_affixes[root]
                #                 for affix in affix_list:
                #                     if affix_of_root == affix:
                #                         return False 


                                



                    
                    


        # print("roots: ",roots,"affixes: ",affixes)
        # for root in roots:
        #     if self.knowledge_base.is_valid_word(root):
        #         root_affixes = self.knowledge_base.get_affixes_for_root(root)
        #         # print(f"roots on ED:{root_affixes}")
        #         if all(affix in root_affixes for affix in affixes):
        #             return True
      
