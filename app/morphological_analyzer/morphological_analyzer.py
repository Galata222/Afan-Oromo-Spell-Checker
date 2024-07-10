from app.knowledge_base.knowledge_base import KnowledgeBase

class MorphologicalAnalyzer:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def analyze(self, word):
        return self.knowledge_base.morphological_analysis(word)
