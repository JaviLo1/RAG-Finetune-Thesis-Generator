#crear vector DataBase

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import json

# Carga los segmentos
with open("segmentos_asignaturas.json", "r", encoding="utf-8") as infile:
    segmentos = json.load(infile)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Chroma vector store (persistente en ./chroma_db)
vectorstore = Chroma.from_texts(segmentos, embeddings, persist_directory="./chroma_db")
