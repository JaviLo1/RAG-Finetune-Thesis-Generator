import csv
import json

# Instrucciones iniciales -> van en el rol "system"
INSTRUCCIONES = (
    "Eres un asesor académico experto en proyectos de tesis. "
    "Tu tarea es generar propuestas de proyectos alineadas con la carrera, intereses y asignaturas indicadas por el estudiante. "
    "Debes estructurar la respuesta con los siguientes apartados: título, descripción, objetivos (en lista numerada), "
    "planificación (en fases detalladas y realistas) y objetivos ODS (claramente relacionados con el proyecto). "
    "Mantén un tono profesional, claro y conciso."
)

def convertir_csv_a_jsonl(csv_path, jsonl_path):
    """
    Convierte un CSV exportado de Google Sheets en un JSONL válido
    para fine-tuning de modelos chat-based (gpt-3.5-turbo).
    Columna G = prompt (input del estudiante).
    Columna H = completion (respuesta esperada).
    """
    with open(csv_path, "r", encoding="utf-8") as csv_file, open(jsonl_path, "w", encoding="utf-8") as jsonl_file:
        reader = csv.reader(csv_file)
        header = next(reader, None)  # saltar encabezado

        for i, row in enumerate(reader, start=2):
            try:
                prompt_raw = row[6].strip()  # Columna G
                completion_raw = row[7].strip()  # Columna H

                if not prompt_raw or not completion_raw:
                    print(f"⚠️ Fila {i} omitida (prompt o completion vacío).")
                    continue

                example = {
                    "messages": [
                        {"role": "system", "content": INSTRUCCIONES},
                        {"role": "user", "content": prompt_raw},
                        {"role": "assistant", "content": completion_raw}
                    ]
                }

                jsonl_file.write(json.dumps(example, ensure_ascii=False) + "\n")

            except IndexError:
                print(f"⚠️ Fila {i} omitida (no hay suficientes columnas).")

    print(f"✅ Archivo JSONL generado con éxito: {jsonl_path}")


if __name__ == "__main__":
    csv_input = "datos_entreno.raw.csv"  # Cambia por el nombre de tu CSV descargado
    jsonl_output = "datos_entreno.jsonl"

    convertir_csv_a_jsonl(csv_input, jsonl_output)

