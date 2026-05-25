# Importamos herramientas para crear nuestro analizador de palabras y frases
import ply.lex as lex     # Esto se encarga de dividir el texto en pedacitos llamados "tokens"
import ply.yacc as yacc   # Esto se encarga de entender cómo se organizan esos tokens (como si fuera gramática)

# === LÉXICO ===
# Vamos a decirle qué palabras o símbolos queremos reconocer

# Esta es la lista de tipos de palabras (tokens) que vamos a entender
tokens = (
    'ID',       # Nombres como 'a', 'promedio', etc.
    'NUMBER',   # Números como 2 o 3.14
    'PLUS',     # El símbolo +
    'MINUS',    # El símbolo -   [NUEVO - PARTE 1]
    'TIMES',    # El símbolo *   [NUEVO - PARTE 1]
    'DIVIDE',   # El símbolo /
    'EQUALS',   # El símbolo =
    'LPAREN',   # El símbolo (
    'RPAREN',   # El símbolo )
    'SEMI',     # El símbolo ;
    'TYPE',     # Las palabras 'int' o 'float'
)

# Estas son las reglas para reconocer símbolos
t_PLUS    = r'\+'
t_MINUS   = r'-'          # Expresión regular para la resta    [NUEVO - PARTE 1]
t_TIMES   = r'\*'         # Expresión regular para la multiplicación [NUEVO - PARTE 1]
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMI    = r';'

# Esta función reconoce los tipos de datos: int o float
def t_TYPE(t):
    r'int|float'
    return t

# Esta función reconoce nombres (como 'a', 'promedio', etc.)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Esta función reconoce números (como 42 o 3.14)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    # Si el número tiene un punto, lo convierte en decimal (float)
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Ignorar espacios, tabulaciones y saltos de línea
t_ignore = ' \t\n'

# Si encuentra algo raro, imprime un mensaje
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Creamos el analizador de palabras
lexer = lex.lex()

# === SINTAXIS ===
# Aquí decimos cómo deben organizarse las palabras

# Estas reglas dicen qué operación tiene prioridad
# PARTE 3: Precedencia correcta — multiplicación y división son más fuertes que suma y resta
# Se define de menor a mayor prioridad (el último tiene mayor prioridad)
precedence = (
    ('left', 'PLUS', 'MINUS'),   # Menor prioridad: + y - se evalúan de izquierda a derecha
    ('left', 'TIMES', 'DIVIDE'), # Mayor prioridad: * y / se evalúan de izquierda a derecha
)

# Esta regla dice cómo se ve una asignación completa
def p_statement_assign(p):
    'statement : TYPE ID EQUALS expression SEMI'
    # Por ejemplo: float promedio = (a + b) / 2;
    p[0] = ('assign', p[1], p[2], p[4])

# PARTE 2: Reglas sintácticas para suma, resta, multiplicación y división
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = (p[2], p[1], p[3])  # Crea un árbol como ('+', algo, algo)

# Esta regla permite usar paréntesis
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Esta regla permite usar números directamente
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

# Esta regla permite usar variables como 'a', 'b'
def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

# PARTE 5: Manejo de errores mejorado — muestra el token problemático claramente
def p_error(p):
    if p:
        print(f"Error de sintaxis cerca de '{p.value}'")
    else:
        print("Error de sintaxis: entrada incompleta o inesperada al final")

# Creamos el analizador de frases (parser)
parser = yacc.yacc()

# === FUNCION PARA IMPRIMIR EL ARBOL BONITO ===
# PARTE 4: Árbol sintáctico visual
def print_pretty_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, tuple):
        # El primer elemento de la tupla suele ser el tipo de nodo
        print(f"{indent}└── {node[0]}")
        for child in node[1:]:
            print_pretty_tree(child, level + 1)
    else:
        # Es un valor hoja (número, string, etc.)
        print(f"{indent}    └── {node}")

# === FUNCIÓN AUXILIAR PARA CORRER UNA PRUEBA ===
def run_test(code, descripcion):
    print("=" * 55)
    print(f"  {descripcion}")
    print("=" * 55)
    print(f"  Entrada: {code}")
    print()

    # Mostrar tokens detectados
    print("  --- TOKENS DETECTADOS ---")
    lexer.input(code)
    for tok in lexer:
        print(f"    {tok}")
    print()

    # Parsear y mostrar árbol
    result = parser.parse(code)
    print("  --- ÁRBOL DE SINTAXIS (AST) ---")
    if result:
        print_pretty_tree(result, level=1)
    else:
        print("    (no se generó árbol por error de sintaxis)")
    print()

# ======================================================
# PARTE 6: PRUEBAS — mínimo 5 ejemplos distintos
# ======================================================

# Prueba 1: Expresión válida con suma
run_test(
    "float x = a + b;",
    "PRUEBA 1 — Suma simple"
)

# Prueba 2: Expresión válida con multiplicación
run_test(
    "int z = a * b;",
    "PRUEBA 2 — Multiplicación simple"
)

# Prueba 3: Expresión con paréntesis
run_test(
    "float promedio = (a + b) / 2;",
    "PRUEBA 3 — Paréntesis y división"
)

# Prueba 4: Expresión compleja (prioridad de operadores)
# Debe interpretarse como: 3 + (5 * 2), NO como (3 + 5) * 2
run_test(
    "float x = 3 + 5 * 2;",
    "PRUEBA 4 — Prioridad de operadores (3 + 5 * 2)"
)

# Prueba 5: Expresión inválida — debe mostrar error claro
run_test(
    "float x = a + ;",
    "PRUEBA 5 — Expresión inválida (error esperado)"
)

# Prueba BONUS: Expresión compleja con todos los operadores y paréntesis anidados
run_test(
    "float resultado = (a + b) * (c - 2) / 4;",
    "PRUEBA BONUS — Expresión compleja con paréntesis anidados"
)