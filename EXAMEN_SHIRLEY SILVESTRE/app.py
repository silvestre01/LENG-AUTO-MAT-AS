
#  Analizador Léxico para Java 
#  En la tabla le añadi la seccion de Atributo, asi lo vi en las diapositivas 

import ply.lex as lex

#  Palabras reservadas 
reserved = {
    'class'     : 'CLASS',
    'public'    : 'PUBLIC',
    'private'   : 'PRIVATE',
    'protected' : 'PROTECTED',
    'static'    : 'STATIC',
    'void'      : 'VOID',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'double'    : 'DOUBLE',
    'boolean'   : 'BOOLEAN',
    'char'      : 'CHAR',
    'String'    : 'STRING_TYPE',
    'if'        : 'IF',
    'else'      : 'ELSE',
    'while'     : 'WHILE',
    'for'       : 'FOR',
    'return'    : 'RETURN',
    'new'       : 'NEW',
}

#  Lista de tokens 
tokens = list(reserved.values()) + [
    # Identificadores y literales
    'ID',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'CARACTER',
    'BOOLEANO',

    # Operadores aritméticos
    'SUMA',        # +
    'RESTA',       # -
    'MULT',        # *
    'DIV',         # /
    'MOD',         # %

    # Operadores relacionales
    'IGUAL_IGUAL', # ==
    'DIFERENTE',   # !=
    'MENOR',       # <
    'MAYOR',       # >
    'MENOR_IGUAL', # <=
    'MAYOR_IGUAL', # >=

    # Operadores lógicos
    'AND',         # &&
    'OR',          # ||
    'NOT',         # !

    # Operadores de asignación
    'IGUAL',       # =
    'SUMA_IGUAL',  # +=
    'RESTA_IGUAL', # -=
    'MULT_IGUAL',  # *=
    'DIV_IGUAL',   # /=

    # Delimitadores
    'PUNTO_COMA',  # ;
    'COMA',        # ,
    'PUNTO',       # .
    'LLAVE_INICIO',    # {
    'LLAVE_FINAL',    # }
    'CORCHETE_INICIO', # [
    'CORCHETE_FINAL', # ]
    'PAREN_INICIO',    # (
    'PAREN_FINAL',    # )

    # Comentarios
    'COMENTARIO_LINEA',
    'COMENTARIO_BLOQUE',
]

#  Reglas simples (orden: más largas primero) 

# Operadores relacionales (2 chars antes que 1 char)
t_IGUAL_IGUAL  = r'=='
t_DIFERENTE    = r'!='
t_MENOR_IGUAL  = r'<='
t_MAYOR_IGUAL  = r'>='
t_AND          = r'&&'
t_OR           = r'\|\|'

# Operadores de asignación compuesta (antes que = simple)
t_SUMA_IGUAL   = r'\+='
t_RESTA_IGUAL  = r'-='
t_MULT_IGUAL   = r'\*='
t_DIV_IGUAL    = r'/='

# Operadores simples
t_SUMA         = r'\+'
t_RESTA        = r'-'
t_MULT         = r'\*'
t_MOD          = r'%'
t_NOT          = r'!'
t_MENOR        = r'<'
t_MAYOR        = r'>'
t_IGUAL        = r'='

# Delimitadores
t_PUNTO_COMA   = r';'
t_COMA         = r','
t_PUNTO        = r'\.'
t_LLAVE_INICIO     = r'\{'
t_LLAVE_FINAL     = r'\}'
t_CORCHETE_INICIO  = r'\['
t_CORCHETE_FINAL  = r'\]'
t_PAREN_INICIO     = r'\('
t_PAREN_FINAL     = r'\)'

# Ignorar espacios y tabulaciones
t_ignore = ' \t\r'

def t_COMENTARIO_BLOQUE(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMENTARIO_LINEA(t):
    r'//[^\n]*'
    return t

def t_DIV(t):
    r'/'
    return t

def t_BOOLEANO(t):
    r'\b(true|false)\b'
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_CARACTER(t):
    r"'([^'\\]|\\.)*'"
    return t

def t_ID(t):
    r'[a-zA-Z_$][a-zA-Z0-9_$]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es palabra reservada
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"  [ERROR] Carácter inválido '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)


# Construcción del lexer 
lexer = lex.lex()


#  Clasificación legible de tokens 
palabras_reservadas = set(reserved.keys())

def tipo_legible(tok_type, tok_value):
    """Devuelve el tipo en español legible."""
    if tok_type in ('ID',):
        return "Identificador"
    elif tok_type in ('ENTERO', 'DECIMAL'):
        return "Número"
    elif tok_type == 'CADENA':
        return "Cadena"
    elif tok_type == 'CARACTER':
        return "Carácter"
    elif tok_type == 'BOOLEANO':
        return "Booleano"
    elif tok_type in ('SUMA','RESTA','MULT','DIV','MOD',
                      'IGUAL_IGUAL','DIFERENTE','MENOR','MAYOR',
                      'MENOR_IGUAL','MAYOR_IGUAL','AND','OR','NOT',
                      'IGUAL','SUMA_IGUAL','RESTA_IGUAL','MULT_IGUAL','DIV_IGUAL'):
        return "Operador"
    elif tok_type in ('PUNTO_COMA','COMA','PUNTO','LLAVE_AB','LLAVE_CE',
                      'CORCHETE_AB','CORCHETE_CE','PAREN_AB','PAREN_CE'):
        return "Delimitador"
    elif tok_type in ('COMENTARIO_LINEA', 'COMENTARIO_BLOQUE'):
        return "Comentario"
    else:
        # Es palabra reservada
        return "Palabra reservada"


def atributo_legible(tok_type, tok_value, tipo_cat):
    """
    Genera el atributo segun la tabla del slide 15:
    - Palabras clave  -> 'Palabra clave'
    - Todo lo demas   -> el lexema original
    """
    if tipo_cat == "Palabra reservada":
        return "Palabra clave"
    return str(tok_value)


def imprimir_tabla(tokens_lista):
    """
    Imprime tabla: Token | Atributo | Tipo | Linea
    Basado en la tabla de ejemplo del slide 15 de la presentacion.
    """
    col1, col2, col3, col4 = 18, 22, 20, 6
    div = "-" * (col1 + col2 + col3 + col4 + 13)

    print(f"\n--- Resultado Del Analisis ---")
    print(f"{'Token':<{col1}} | {'Atributo':<{col2}} | {'Tipo':<{col3}} | {'Linea'}")
    print(div)

    for token_val, tok_type, tipo, linea in tokens_lista:
        tk  = str(tok_type)
        atr = atributo_legible(tok_type, token_val, tipo)
        if len(tk)  > col1 - 1: tk  = tk[:col1-4]  + "..."
        if len(atr) > col2 - 1: atr = atr[:col2-4] + "..."
        print(f"{tk:<{col1}} | {atr:<{col2}} | {tipo:<{col3}} | {linea}")

    print(div)
    print(f"Total de tokens: {len(tokens_lista)}\n")


def analizar(codigo):
    """Tokeniza el código Java y devuelve la lista de tokens."""
    lexer.lineno = 1
    lexer.input(codigo)

    resultado = []
    for tok in lexer:
        tipo = tipo_legible(tok.type, tok.value)
        # (valor_original, tipo_interno, tipo_legible, linea)
        resultado.append((str(tok.value), tok.type, tipo, tok.lineno))

    return resultado


#  Código Java de prueba que se analiza al iniciar el programa
codigo_prueba = '''\
public class Hola {
    public static void main(String[] args) {
        int x = 10;
        if (x > 5) {
            System.out.println("Mayor que 5");
        } else {
            System.out.println("Menor o igual a 5");
        }
        
    }
}
'''

#  Main 
if __name__ == "__main__":
    print("=" * 70)
    print("        ANALIZADOR LÉXICO PARA JAVA — usando PLY")
    print("=" * 70)

    # Analizar el programa de prueba
    print("\n>>> Analizando programa de prueba...\n")
    tokens_prueba = analizar(codigo_prueba)
    imprimir_tabla(tokens_prueba)

    # Modo interactivo 
    print("=" * 70)
    print("  MODO INTERACTIVO")
    print("  Ingresa código Java línea por línea.")
    print("  Escribe una línea en blanco para analizar el bloque.")
    print("  Escribe 'salir' para terminar.")
    print("=" * 70)

    while True:
        print("\nIngresa código Java (línea vacía para analizar | 'salir' para salir):")
        lineas = []

        while True:
            try:
                linea = input("  > ")
            except EOFError:
                linea = "salir"

            if linea.strip().lower() == "salir":
                print("\nSaliendo del analizador. ¡Hasta luego!")
                exit(0)

            if linea == "":
                break

            lineas.append(linea)

        if not lineas:
            print("  (No se ingresó código)")
            continue

        codigo_usuario = "\n".join(lineas)
        print()
        resultado = analizar(codigo_usuario)

        if resultado:
            imprimir_tabla(resultado)
        else:
            print("  No se encontraron tokens válidos.\n")