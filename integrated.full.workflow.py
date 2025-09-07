# generate_thesis_chunks_log.py
# Igual que antes, pero además guarda prompt + output en un archivo de log .txt

from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os
import sys
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")
FT_MODEL_ID = "ft:gpt-3.5-turbo-0125:wbw::CBOnWovA"
CHROMA_PERSIST_DIR = "./RAG_Model/chroma_db"
TOP_K = 3
MAX_CHARS_PER_CHUNK = 4000

SYSTEM_INSTRUCTIONS = (
    "Eres un asesor académico experto en proyectos de tesis. "
    "Tu tarea es generar propuestas de proyectos alineadas con la carrera, intereses y asignaturas indicadas por el estudiante. "
    "Debes estructurar la respuesta con los siguientes apartados: título, descripción, objetivos (en lista numerada), "
    "planificación (en fases detalladas y realistas) y objetivos ODS (claramente relacionados con el proyecto). "
    "Mantén un tono profesional, claro y conciso."
)

client = OpenAI(api_key=API_KEY)

def load_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    return Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)

def get_top_k_chunks(vectorstore, query: str, k: int = TOP_K):
    results = vectorstore.similarity_search(query, k=k)
    chunks = []
    for doc in results:
        content = (doc.page_content or "").strip()
        if len(content) > MAX_CHARS_PER_CHUNK:
            content = content[:MAX_CHARS_PER_CHUNK] + "\n[...]"
        chunks.append(content)
    return chunks

def build_user_prompt(carrera: str, gustos: str, tecnologias: str, chunks):
    header = (
        f"Perfil del estudiante:\n"
        f"- Carrera: {carrera or '-'}\n"
        f"- Gustos/Intereses: {gustos or '-'}\n"
        f"- Tecnologías: {tecnologias or '-'}\n\n"
        f"Asignaturas más relacionadas (contenido completo):\n"
    )
    cuerpo = "\n\n".join([f"### Asignatura {i+1}\n{ch}" for i, ch in enumerate(chunks)])
    return f"{header}\n{cuerpo}\n\nGenera una propuesta de TFM siguiendo la estructura requerida."

def infer_ft_model(user_msg: str) -> str:
    """
    Llama al modelo fine-tuneado con system+user y devuelve el texto generado.
    """
    resp = client.chat.completions.create(
        model=FT_MODEL_ID,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.4
    )
    return resp.choices[0].message.content

def save_to_log(prompt: str, output: str):
    """
    Guarda el prompt completo y la respuesta del modelo en un archivo de log .txt
    con timestamp para no sobrescribir.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tfm_propuesta_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== PROMPT COMPLETO ===\n")
        f.write(prompt + "\n\n")
        f.write("=== RESPUESTA DEL MODELO ===\n")
        f.write(output + "\n")
    print(f"📁 Prompt y salida guardados en: {filename}")

def main():
    carrera = "Ingenieria Quimica"
    gustos = "Programacion, reactores nucleares, seguridad"
    tecnologias = "reactores nucleares, IA"

    if not any([carrera, gustos, tecnologias]):
        print("❌ Debes introducir al menos un campo del perfil.")
        return

    vectorstore = load_vectorstore()
    query_text = "\n".join(filter(None, [
        f"Carrera: {carrera}" if carrera else "",
        f"Gustos: {gustos}" if gustos else "",
        f"Tecnologías: {tecnologias}" if tecnologias else ""
    ])).strip()

    chunks = get_top_k_chunks(vectorstore, query_text, k=TOP_K)
    if not chunks:
        print("⚠️ No se encontraron resultados en la RAG DB.")
        return

    user_prompt = build_user_prompt(carrera, gustos, tecnologias, chunks)
    output = infer_ft_model(user_prompt)

    print("\n=== Propuesta de TFM ===\n")
    print(output)
    print("\n=========================\n")

    save_to_log(user_prompt, output)

if __name__ == "__main__":
    main()
