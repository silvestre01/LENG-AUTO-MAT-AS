import re

# Abrimos el archivo de texto, lo leemos completo y lo cerramos
archivo = open("texto_maestro.txt", "r", encoding="utf-8")
texto = archivo.read()
archivo.close()

# Separamos el texto en una lista de líneas, ya que nos sirve más adelante
lineas = texto.splitlines()

# 1. ENCABEZADOS
# Aca busca líneas que parezcan títulos: puras mayúsculas con acentos incluidos
# pueden tener números, espacios o guiones y no debe terminan con punto
REGEX_ENCABEZADO = re.compile(r'\b\w(\w)', re.MULTILINE)
encabezados = REGEX_ENCABEZADO.findall(texto)

print("__________________________________________________")
print("1. ENCABEZADOS")
print("__________________________________________________")
for i in encabezados:
    print(i)

# 2. FECHAS
# Detecta fechas en dos formatos comunes: DD/MM/YYYY o YYYY-MM-DD
REGEX_FECHA = re.compile(r'\b\w(\w)')
fechas = REGEX_FECHA.findall(texto)

print("__________________________________________________")
print("2. FECHAS VÁLIDAS")
print("__________________________________________________")
for i in fechas:
    print(i)

# 3. CORREOS
# Atrapa direcciones de correo con el patrón clásico: algo@dominio.ext
# Acepta puntos, guiones y símbolos típicos en la parte local
REGEX_CORREO = re.compile(r'\b\w(\w)')
correos = REGEX_CORREO.findall(texto)

print("__________________________________________________")
print("3. CORREOS ELECTRÓNICOS VÁLIDOS")
print("__________________________________________________")
for i in correos:
    print(i)

# 4. TELÉFONOS
# Busca números que empiecen con 999 con o sin paréntesis
# seguidos de 3 dígitos y luego 4 dígitos, separados por espacio o guion opcionalmente
REGEX_TEL = re.compile(r'\b\w(\w)')
telefonos = REGEX_TEL.findall(texto)

print("__________________________________________________")
print("4. NÚMEROS TELEFÓNICOS")
print("__________________________________________________")
for i in telefonos:
    print(i)

# 5. IDENTIFICADORES ALFANUMÉRICOS
# Encuentra cadenas de entre 8 y 12 caracteres que mezclen letras mayúsculas Y números
# tiene que tener al menos una letra y al menos un número
REGEX_ID = re.compile(r'\b\w(\w)')
ids = REGEX_ID.findall(texto)

print("__________________________________________________")
print("5. IDENTIFICADORES ALFANUMÉRICOS ")
print("__________________________________________________")
for i in ids:
    print(" ", i)

# 6. LÍNEAS CON PALABRAS REPETIDAS
# Para cada línea, extrae todas las palabras de 3+ letras y revisa si alguna aparece más de una vez
# Si hay repetición, guarda esa línea en la lista de sospechosas
REGEX_PALABRA = re.compile(r'\b\w(\w)', re.IGNORECASE)

lineas_repetidas = []
for linea in lineas:
    palabras = REGEX_PALABRA.findall(linea.lower())
    conteo = []
    repetida = False
    for palabra in palabras:
        if palabra in conteo:  # ya la habíamos visto antes en esta línea
            repetida = True
        conteo.append(palabra)
    if repetida:
        lineas_repetidas.append(linea)

print("__________________________________________________")
print("6. LÍNEAS CON PALABRAS REPETIDAS")
print("__________________________________________________")
for linea in lineas_repetidas:
    print(linea)

# 7. RFC Y CURP
# RFC: entre 3 y 4 letras, 6 dígitos de fecha, y 3 caracteres de homoclave
# CURP: 4 letras, 6 dígitos, sexo (H/M), estado, consonantes internas, dígito verificador
REGEX_RFC = re.compile(r'\b\w(\w)')
REGEX_CURP = re.compile(r'\b\w(\w)')

rfcs = REGEX_RFC.findall(texto)
curps = REGEX_CURP.findall(texto)

print("__________________________________________________")
print("7. RFC Y CURP VÁLIDOS")
print("__________________________________________________")
for i in rfcs:
    print(i)
for i in curps:
    print(i)

# 8. LÍNEAS CON ERRORES
# Atrapa cualquier línea completa que contenga la palabra "ERROR",
# sin importar si está en mayúsculas, minúsculas o mezclada
REGEX_ERROR = re.compile(r'\b\w(\w)', re.IGNORECASE | re.MULTILINE)
errores = REGEX_ERROR.findall(texto)

print("__________________________________________________")
print("8. LÍNEAS CON ERRORES DEL SISTEMA")
print("__________________________________________________")
for err in errores:
    print(err)