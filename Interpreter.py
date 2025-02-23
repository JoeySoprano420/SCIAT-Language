class TokenType:
    DEFINE = "DEFINE"
    EXECUTE = "EXECUTE"
    LOOP = "LOOP"
    RUN = "RUN"
    CHECK = "CHECK"
    FINALIZE = "FINALIZE"
    SAVE = "SAVE"
    CALLFUNC = "CALLFUNC"
    MAP = "MAP"
    IDENTIFIER = "IDENTIFIER"
    SYMBOL = "SYMBOL"
    STRING = "STRING"
    NUMBER = "NUMBER"
    ARROW = "ARROW"
    SEPARATOR = "SEPARATOR"

import re

def tokenize(code):
    tokens = []
    token_specification = [
        (TokenType.DEFINE, r';DEFINE'),
        (TokenType.EXECUTE, r';EXECUTE'),
        (TokenType.LOOP, r';LOOP'),
        (TokenType.RUN, r';RUN'),
        (TokenType.CHECK, r';CHECK'),
        (TokenType.FINALIZE, r';FINALIZE'),
        (TokenType.SAVE, r';SAVE'),
        (TokenType.CALLFUNC, r';CALLFUNC'),
        (TokenType.MAP, r';MAP'),
        (TokenType.ARROW, r'\u2192'),
        (TokenType.IDENTIFIER, r'\w+'),
        (TokenType.STRING, r'".*?"'),
        (TokenType.NUMBER, r'\d+'),
        (TokenType.SYMBOL, r'[:;\[\]{}(),]'),
        (TokenType.SEPARATOR, r'\s+'),
    ]
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind != TokenType.SEPARATOR:  # Ignore whitespace
            tokens.append((kind, value))
    return tokens

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []
    
    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, {self.children})"

def parse(tokens):
    ast = []
    index = 0
    
    while index < len(tokens):
        try:
            kind, value = tokens[index]
            if kind in {TokenType.DEFINE, TokenType.EXECUTE, TokenType.LOOP, TokenType.RUN, TokenType.CHECK, TokenType.FINALIZE, TokenType.SAVE}:
                node = ASTNode(kind, value)
                index += 1
                while index < len(tokens) and tokens[index][0] in {TokenType.IDENTIFIER, TokenType.STRING, TokenType.NUMBER, TokenType.SYMBOL}:
                    node.children.append(ASTNode(tokens[index][0], tokens[index][1]))
                    index += 1
                ast.append(node)
            else:
                raise ValueError(f"Unexpected token: {value}")
        except Exception as e:
            print(f"Parsing error at token {index}: {e}")
            break
    
    return ast

def interpret(ast):
    for node in ast:
        try:
            if node.type == TokenType.DEFINE:
                print(f"Defining task: {node.children}")
            elif node.type == TokenType.EXECUTE:
                print(f"Executing: {node.children}")
            elif node.type == TokenType.LOOP:
                print(f"Looping with parameters: {node.children}")
            elif node.type == TokenType.RUN:
                print(f"Running: {node.children}")
            elif node.type == TokenType.CHECK:
                print(f"Checking: {node.children}")
            elif node.type == TokenType.FINALIZE:
                print(f"Finalizing: {node.children}")
            elif node.type == TokenType.SAVE:
                print(f"Saving result to: {node.children}")
            else:
                raise ValueError(f"Unknown command: {node.type}")
        except Exception as e:
            print(f"Interpretation error: {e}")

code_sample = """
;DEFINE :task(load_data) → ;MAP[loc = "/data/input.csv"]
;EXECUTE :task(load_data) → ;CALLFUNC(parse_csv, :loc)
;LOOP (i : 0 → 10) {
    ;RUN process_chunk(:i) → ;CHECK result
}
;FINALIZE → ;SAVE result → "/data/output.bin"
"""

tokens = tokenize(code_sample)
ast = parse(tokens)
interpret(ast)
