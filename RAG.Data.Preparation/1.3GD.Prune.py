#Realiza limpiado de tramos de texto inecesario en guia docente.txt
#2a fase limpieza

import re

def limpiar_bloque_datos_descriptivos(bloque):
    """
    Dado un bloque de '1. Datos descriptivos de la asignatura', devuelve solo:
    - La línea de Asignatura
    - El bloque Departamento/s
    - El bloque Área/s de conocimiento
    """
    lineas = bloque.splitlines()
    resultado = []

    capturando_departamento = False
    capturando_area = False

    for linea in lineas:
        # Asignatura
        if linea.startswith("Asignatura:"):
            resultado.append(linea)
        # Departamento
        elif linea.startswith("- Departamento/s:"):
            capturando_departamento = True
            resultado.append(linea)
        elif capturando_departamento:
            if linea.startswith("- ") and not linea.startswith("- Área/s de conocimiento:"):
                capturando_departamento = False
            else:
                resultado.append(linea)
                continue
        # Área/s de conocimiento
        if linea.startswith("- Área/s de conocimiento:"):
            capturando_area = True
            resultado.append(linea)
        elif capturando_area:
            if linea.startswith("- "):  # Nueva sección, termina área
                capturando_area = False
            elif linea.strip() != "":
                resultado.append(linea)
                continue

    # Elimina líneas vacías adicionales
    return "\n".join([l for l in resultado if l.strip() != ""])

# Leemos el archivo completo
with open("guia_docente_filtrada.txt", "r", encoding="utf-8") as infile:
    texto = infile.read()

# Usamos regex para encontrar cada bloque de "1. Datos descriptivos..." hasta el siguiente bloque numerado o fin
patron = re.compile(
    r'(1\. Datos descriptivos de la asignatura[\s\S]*?)(?=(?:\n\d+\. )|\Z)', re.MULTILINE)

resultado = []
ultimo_fin = 0

for match in patron.finditer(texto):
    start, end = match.span()
    # Añadir texto entre bloques (apartados 6, 10 y otros) tal cual
    if start > ultimo_fin:
        resultado.append(texto[ultimo_fin:start])
    bloque = match.group(1)
    bloque_limpio = limpiar_bloque_datos_descriptivos(bloque)
    resultado.append(bloque_limpio)
    ultimo_fin = end

# Añadir cualquier texto restante (por ejemplo, si el último bloque no era 1.)
if ultimo_fin < len(texto):
    resultado.append(texto[ultimo_fin:])

texto_final = "".join(resultado)

with open("guia_docente_final.txt", "w", encoding="utf-8") as outfile:
    outfile.write(texto_final)

print("Limpieza quirúrgica completada. 6 y 10 permanecen intactos.")
