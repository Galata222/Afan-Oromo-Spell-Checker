import re

def tokenize(text):
    # Define a regular expression for tokenizing words (possibly followed by a punctuation mark), digits, and standalone punctuation marks
    pattern = re.compile(r'\b[\w\'-]+(?:[.,;:!?\"\'])?\b|\d+|[.,;:!?()\"\']|\s')
    text = text.lower()

    # Use the regular expression to find all tokens in the input text
    tokens = pattern.findall(text)

    # Filter out punctuation marks and digits from the list of tokens
    tokens = [token for token in tokens if not re.match(r'^[.,;:!?()\"\']+$', token) and not token.isdigit()]

    return tokens
