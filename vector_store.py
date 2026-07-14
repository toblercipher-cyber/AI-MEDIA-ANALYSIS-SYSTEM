import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceBgeEmbeddings(
        model_name=EMBEDDING_MODEL, 
        model_kwargs={
            "device": "cpu"
        },
        cache_folder="./embeddings_cache"  # ✅ Add this
    )

def build_vector_store(transcript: str) -> Chroma:
    print("Building vector store...")

    splitter = RecursiveCharacterTextSplitter(  # ✅ fixed indentation
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(transcript)

    docs = [
        Document(page_content=chunk, metadata={'chunk_index': i})  # ✅ fixed missing closing bracket
        for i, chunk in enumerate(chunks)  # ✅ fixed typo: enumarate -> enumerate
    ]

    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(  # ✅ fixed: {} -> ()
        documents=docs,
        embedding=embeddings,  # ✅ fixed: embeddings -> embedding
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )

    return vector_store  # ✅ fixed indentation


def load_vector_store() -> Chroma:
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR  # ✅ fixed typo: persist_irectory -> persist_directory
    )
    return vector_store

def get_retriever(vector_store: Chroma, k: int = 4):
    return vector_store.as_retriever(
        search_type='mmr',
        search_kwargs={"k": k}
    )


