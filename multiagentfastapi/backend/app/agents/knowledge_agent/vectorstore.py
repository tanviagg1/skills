from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_DIR = Path(__file__).parent.parent.parent.parent / "chroma_db"
CHROMA_DIR.mkdir(exist_ok=True)
COLLECTION_NAME = "documents"

# Local embeddings — runs on your machine, no API key needed
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
)

# Singleton — reuse the same instance so indexing and querying share the same connection
_vectorstore: Chroma | None = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR),
        )
    return _vectorstore
