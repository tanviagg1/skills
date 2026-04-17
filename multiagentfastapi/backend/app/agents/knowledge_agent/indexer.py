from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vectorstore import get_vectorstore

UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


def load_document(file_path: Path) -> list:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif suffix in (".txt", ".md"):
        loader = TextLoader(str(file_path), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    return loader.load()


def index_file(file_path: Path) -> int:
    """Load, chunk, embed and store a file. Returns number of chunks stored."""
    docs = load_document(file_path)
    chunks = splitter.split_documents(docs)

    # Add source metadata
    for chunk in chunks:
        chunk.metadata["source_file"] = file_path.name

    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    return len(chunks)


def get_indexed_files() -> list[str]:
    """Return list of all indexed file names."""
    vectorstore = get_vectorstore()
    collection = vectorstore._collection
    results = collection.get(include=["metadatas"])
    files = {m.get("source_file", "unknown") for m in results["metadatas"]}
    return sorted(files)
