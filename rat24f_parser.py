# rat24f_parser.py
class Rat24FParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    @property
    def current_token(self):
        return self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None

    def advance(self):
        self.current_token_index += 1

    def match(self, expected_type, expected_lexeme=None):
        if self.current_token is None:
            raise SyntaxError(f"Expected {expected_type} '{expected_lexeme}' but found end of input.")
        if self.current_token.type == expected_type and (expected_lexeme is None or self.current_token.lexeme == expected_lexeme):
            self.advance()
        else:
            raise SyntaxError(f"Expected {expected_type} '{expected_lexeme}' but found '{self.current_token.lexeme}'.")

    def parse(self):
        ast = []
        while self.current_token is not None:
            if self.current_token.type == "KEYWORD" and self.current_token.lexeme == "integer":
                ast.append(self.parse_declaration())
            elif self.current_token.type == "IDENTIFIER":
                ast.append(self.parse_assignment())
            elif self.current_token.type == "KEYWORD" and self.current_token.lexeme == "while":
                ast.append(self.parse_while())
            elif self.current_token.type == "KEYWORD" and self.current_token.lexeme == "put":
                ast.append(self.parse_output())
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token.lexeme}")
        return ast

    def parse_declaration(self):
        self.match("KEYWORD", "integer")
        identifiers = []
        while self.current_token.type == "IDENTIFIER":
            identifiers.append(self.current_token.lexeme)
            self.advance()
            if self.current_token and self.current_token.lexeme == ",":
                self.advance()
            else:
                break
        self.match("DELIMITER", ";")
        return {"type": "declaration", "data_type": "integer", "identifiers": identifiers}

    def parse_assignment(self):
        left = self.current_token.lexeme
        self.advance()
        self.match("ASSIGN", "=")
        right = self.parse_expression()
        self.match("DELIMITER", ";")
        return {"type": "assignment", "left": left, "right": right}

    def parse_expression(self):
        left = None
        if self.current_token.type == "INTEGER":
            left = {"type": "literal", "value": int(self.current_token.lexeme)}
            self.advance()
        elif self.current_token.type == "IDENTIFIER":
            left = {"type": "identifier", "name": self.current_token.lexeme}
            self.advance()
        else:
            raise SyntaxError(f"Invalid expression: {self.current_token.lexeme}")

        if self.current_token and self.current_token.type == "OPERATOR":
            operator = self.current_token.lexeme
            self.advance()
            right = self.parse_expression()
            return {"type": "binary_op", "operator": operator, "left": left, "right": right}

        return left

    def parse_while(self):
        self.match("KEYWORD", "while")
        self.match("DELIMITER", "(")
        condition = self.parse_expression()
        self.match("DELIMITER", ")")
        self.match("DELIMITER", "{")
        body = []
        while self.current_token and self.current_token.lexeme != "}":
            if self.current_token.type == "KEYWORD" and self.current_token.lexeme in ["integer", "put", "while"]:
                if self.current_token.lexeme == "integer":
                    body.append(self.parse_declaration())
                elif self.current_token.lexeme == "put":
                    body.append(self.parse_output())
                elif self.current_token.lexeme == "while":
                    body.append(self.parse_while())
            elif self.current_token.type == "IDENTIFIER":
                body.append(self.parse_assignment())
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token.lexeme}")
        self.match("DELIMITER", "}")
        return {"type": "while", "condition": condition, "body": body}

    def parse_output(self):
        self.match("KEYWORD", "put")
        self.match("DELIMITER", "(")
        value = self.parse_expression()
        self.match("DELIMITER", ")")
        self.match("DELIMITER", ";")
        return {"type": "output", "value": value}
