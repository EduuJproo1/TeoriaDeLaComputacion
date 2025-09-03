import re

# Palabras clave
KEYWORDS = {'if', 'else', 'while', 'return', 'int', 'float', 'bool'}

# Definición de tokens
TOKEN_SPECIFICATION = [
    ('STRING',    r'"[^"\n]*"'),                  # Cadena entre comillas dobles
    ('COMMENT',   r'(//.*|#.*)'),                 # Comentarios de línea
    ('INCREMENT', r'\+\+'),                       # Operador incremento
    ('DECREMENT', r'--'),                         # Operador decremento
    ('OP_EQ',     r'=='),                         # Igualdad
    ('OP_ASSIGN', r'='),                          # Asignación
    ('OP_PLUS',   r'\+'),                         # Suma
    ('OP_MINUS',  r'-'),                          # Resta
    ('OP_MUL',    r'\*'),                         # Multiplicación
    ('OP_DIV',    r'/'),                          # División
    ('NUMBER',    r'\b\d+(\.\d+)?\b'),            # Número entero o decimal
    ('IDENT',     r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'), # Identificador válido
    ('LPAREN',    r'\('),                         # Paréntesis izquierdo
    ('RPAREN',    r'\)'),                         # Paréntesis derecho
    ('LBRACE',    r'\{'),                         # Llave izquierda
    ('RBRACE',    r'\}'),                         # Llave derecha
    ('SEMICOLON', r';'),                          # Punto y coma
    ('WHITESPACE',r'\s+'),                        # Espacios y saltos de línea
    ('UNKNOWN',   r'.'),                          # Carácter desconocido (error léxico)
]

# Compilar expresiones regulares en una sola expresión
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)
token_pattern = re.compile(token_regex)

def lexer(code):
    tokens = []
    line_num = 1
    line_start = 0

    for mo in token_pattern.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        if kind == 'WHITESPACE':
            if '\n' in value:
                line_num += value.count('\n')
                line_start = mo.end()
            continue
        elif kind == 'COMMENT':
            continue
        elif kind == 'IDENT' and value in KEYWORDS:
            kind = 'KEYWORD'
        elif kind == 'UNKNOWN':
            raise SyntaxError(f'Error léxico: carácter inesperado "{value}" en línea {line_num}, columna {column}')

        tokens.append((kind, value, line_num, column))

    return tokens

# Prueba de lexer
if __name__ == '__main__':
    test_code = '''
    int x = 10;
    if (x == 10) {
        x = x + 1;
        // incremento
        x++;
    }
    '''

    result = lexer(test_code)
    for kind, value, line, column in result:
        print(f'{kind:12} | {value:8} | línea {line}, columna {column}')