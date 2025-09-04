import re

# Palabras clave
KEYWORDS = {'if', 'else', 'while', 'return', 'int', 'float', 'bool'}

# Definición de tokens
TOKEN_SPECIFICATION = [
    ('STRING',     r'"([^"\\\n]|\\.)*"'),          # Cadenas string
    ('COMMENT',    r'(//.*|#.*)'),                 # Comentarios de línea
    
    # Operadores especiales
    ('INCREMENT',  r'\+\+'),                       # ++
    ('DECREMENT',  r'--'),                         # --
    
    # Operadores lógicos y relacionales
    ('OP_AND',     r'&&'),                         # &&
    ('OP_OR',      r'\|\|'),                       # ||
    ('OP_NEQ',     r'!='),                         # !=
    ('OP_LTE',     r'<='),                         # <=
    ('OP_GTE',     r'>='),                         # >=
    ('OP_EQ',      r'=='),                         # ==
    ('OP_NOT',     r'!'),                          # !
    ('OP_LT',      r'<'),                          # <
    ('OP_GT',      r'>'),                          # >

    # Operadores matemáticos y asignación
    ('OP_ASSIGN',  r'='),                          # =
    ('OP_PLUS',    r'\+'),                         # +
    ('OP_MINUS',   r'-'),                          # -
    ('OP_MUL',     r'\*'),                         # *
    ('OP_DIV',     r'/'),                          # /

    # Operador ternario y concatenación
    ('OP_TERNARY', r'\?|:'),                       # ? y :
    ('DOT',        r'\.'),                         # .

    # Tokens generales
    ('NUMBER',     r'\b\d+(\.\d+)?\b'),            # Números enteros y decimales
    ('IDENT',      r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'), # Identificadores
    ('LPAREN',     r'\('),                         # (
    ('RPAREN',     r'\)'),                         # )
    ('LBRACE',     r'\{'),                         # {
    ('RBRACE',     r'\}'),                         # }
    ('SEMICOLON',  r';'),                          # ;
    ('WHITESPACE', r'\s+'),                        # Espacios y saltos
    ('UNKNOWN',    r'.'),                          # Cualquier carácter no reconocido
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
    archivo = 'entrada.txt'

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            codigo_fuente = f.read()

        resultado = lexer(codigo_fuente)

        print(f'Análisis léxico del archivo: {archivo}\n')
        for tipo, valor, linea, columna in resultado:
            print(f'{tipo:12} | {valor:10} | línea {linea}, columna {columna}')

    except FileNotFoundError:
        print(f'Error: No se encontró el archivo "{archivo}".')
