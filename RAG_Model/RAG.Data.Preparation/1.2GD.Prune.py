#Realiza limpiado de tramos de texto inecesario en guia docent.txt
#1a fase limpieza
import re

# Secciones de inicio y fin para extracción principal
start_points = [
    "1. Datos descriptivos de la asignatura",
    "6. Contenidos de la asignatura",
    "10. Resultados de Aprendizaje"
]
end_points = [
    "2. Requisitos de matrícula y calificación",
    "7. Metodología y volumen de trabajo del estudiante",
    "11. Cronograma / calendario de la asignatura"
]

start_pattern = re.compile(
    r"^(1\. Datos descriptivos de la asignatura|6\. Contenidos de la asignatura|10\. Resultados de Aprendizaje)",
    re.MULTILINE)
end_pattern = re.compile(
    r"^(2\. Requisitos de matrícula y calificación|7\. Metodología y volumen de trabajo del estudiante|11\. Cronograma / calendario de la asignatura)",
    re.MULTILINE)

# 1. Quitar los bloques "--- Página ... Página ..."
def remove_page_blocks(text):
    # Busca bloques que empiezan con "--- Página" y acaban en una línea que empiece por "Página "
    pattern = re.compile(
        r"--- Página.*?(?:\nPágina [^\n]*\n)", re.DOTALL)
    return re.sub(pattern, '', text)

# 2. Extracción de bloques de interés
def extract_sections(text):
    extracted_sections = []
    for match in start_pattern.finditer(text):
        start_idx = match.start()
        end_match = end_pattern.search(text, match.end())
        end_idx = end_match.start() if end_match else len(text)
        section = text[start_idx:end_idx].strip()
        extracted_sections.append(section)
    return extracted_sections

# MAIN
with open("guia_docente.txt", "r", encoding="utf-8") as infile:
    text = infile.read()

# 1. Limpieza de bloques de páginas
clean_text = remove_page_blocks(text)

# 2. Extracción de bloques de interés
sections = extract_sections(clean_text)

# 3. Guardar resultado
with open("guia_docente_filtrada2.txt", "w", encoding="utf-8") as outfile:
    outfile.write("\n\n".join(sections))

print("Extracción y limpieza completa. Revisa 'guia_docente_filtrada2.txt'")
