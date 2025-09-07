#Test rápido para Vector DB (model RAG)
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set") = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Load the existing vector store from your persist directory
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
print("Chroma vector store loaded.\n")

# Test with a sample student profile (you can run this multiple times)
while True:
    consulta = input("example text here")
    if not consulta.strip():
        break

    # Search for the top 3 most relevant segmentsi
    print("Buscando los segmentos más relevantes...")

    resultados = vectorstore.similarity_search(consulta, k=3)

    print("\nTop 3 results:\n")
    for i, doc in enumerate(resultados, 1):
        print(f"--- Result {i} ---")
        print(doc.page_content[:700])  # Show the first 700 chars for clarity
        print("-" * 40)
