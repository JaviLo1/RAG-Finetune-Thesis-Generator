#crea modelo finetuning openAI

from openai import OpenAI

# ⚠️ Sustituye con tu API key de OpenAI
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")
  
client = OpenAI(api_key=API_KEY)

# Archivo JSONL de entrenamiento
JSONL_FILE = "datos_entreno.jsonl"
MODELO_BASE = "gpt-3.5-turbo"  # Modelo base para fine-tuning

def subir_y_finetunear():
    # 1️⃣ Subir archivo
    print("Subiendo archivo de entrenamiento...")
    archivo = client.files.create(
        file=open(JSONL_FILE, "rb"),
        purpose="fine-tune"
    )
    file_id = archivo.id
    print(f"✅ Archivo subido con éxito. File ID: {file_id}")

    # 2️⃣ Crear fine-tuning
    print("Creando fine-tune...")
    fine_tune = client.fine_tuning.jobs.create(
        training_file=file_id,
        model=MODELO_BASE
    )
    fine_tune_id = fine_tune.id
    print(f"🚀 Fine-tune iniciado. Fine-tune Job ID: {fine_tune_id}")

    print("\nℹ️ Para monitorear el progreso puedes usar en Python:")
    print(f"client.fine_tuning.jobs.retrieve('{fine_tune_id}')")
    print("o listar todos con: client.fine_tuning.jobs.list()")

if __name__ == "__main__":
    subir_y_finetunear()
