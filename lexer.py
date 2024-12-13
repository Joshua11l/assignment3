import re

class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        token_specification = [
            ("KEYWORD", r'\b(if|else|while|get|put|integer|boolean|real|true|false)\b'),
            ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ("INTEGER", r'\b\d+\b'),
            ("ASSIGN", r'='),
            ("OPERATOR", r'[+\-*/<>]=?|!='),
            ("DELIMITER", r'[;{},()]'),
            ("WHITESPACE", r'\s+'),
            ("COMMENT", r'\[\*.*?\*\]')
        ]
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

        for match in re.finditer(token_regex, self.code):
            kind = match.lastgroup
            lexeme = match.group()
            if kind not in ("WHITESPACE", "COMMENT"):
                self.tokens.append(Token(kind, lexeme))
        return self.tokens
