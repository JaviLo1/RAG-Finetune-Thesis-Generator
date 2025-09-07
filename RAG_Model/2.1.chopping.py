import re
import json

# 1. Leer el archivo procesado
with open("guia_docente_final.txt", "r", encoding="utf-8") as infile:
    texto = infile.read()

# 2. Chopping: un segmento por asignatura
# El patrón busca cada vez que empieza una nueva asignatura en una línea nueva
segmentos = re.split(r'(?=^Asignatura:)', texto, flags=re.MULTILINE)
segmentos = [seg.strip() for seg in segmentos if seg.strip()]

print(f"Segmentos por asignatura detectados: {len(segmentos)}")

# 3. Guardar todos los segmentos juntos en un JSON
with open("segmentos_asignaturas.json", "w", encoding="utf-8") as outjson:
    json.dump(segmentos, outjson, ensure_ascii=False, indent=2)
print("Todos los segmentos guardados en 'segmentos_asignaturas.json'.")

# 4. Guardar cada segmento por separado en un archivo .txt
for i, seg in enumerate(segmentos, 1):
    nombre_archivo = f"asignatura_{i}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as outfile:
        outfile.write(seg)
print(f"Segmentos guardados en archivos 'asignatura_#.txt'.")

