# import os
# from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredPowerPointLoader

# CHROMA_EXT = "external_vector_db"
# COLLECTION_NAME = "external_docs"
# EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# def get_embeddings():
#     return HuggingFaceBgeEmbeddings(
#         model_name=EMBEDDING_MODEL, 
#         model_kwargs={
#             "device": "cpu"
#         },
#         cache_folder="./embeddings_cache"  # ✅ Add this
#     )

# def load_document(file_path: str):
#     ext = os.path.splitext(file_path)[1].lower()
#     loaders = {
#         ".pdf":  PyPDFLoader,
#         ".docx": Docx2txtLoader,
#         ".txt":  lambda p: TextLoader(p, encoding="utf-8"),
#         ".pptx": UnstructuredPowerPointLoader
#     }
#     if ext not in loaders:
#         raise ValueError(f"Unsupported file type: {ext}")
#     return loaders[ext](file_path).load()

# def build_vector_store(file_path: str) -> Chroma:
#     print("Building vector store...")
#     docs = load_document(file_path)
#     chunks = splitter.split_documents(docs)
#     return Chroma.from_documents(
#         documents=chunks,
#         embedding=get_embeddings(),
#         collection_name=COLLECTION_NAME,
#         persist_directory=CHROMA_EXT
#     )

# def load_vector_store() -> Chroma:
#     return Chroma(
#         collection_name=COLLECTION_NAME,
#         embedding_function=get_embeddings(),
#         persist_directory=CHROMA_EXT
#     )

# def get_retriever(vector_store: Chroma, k: int = 4):
#     return vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k})









import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredPowerPointLoader

CHROMA_EXT = "external_vector_db"
COLLECTION_NAME = "external_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ============================================================
# ADAPTIVE SPLITTER - Based on file size
# ============================================================

def get_splitter_for_file(file_path: str):
    """Get chunk size based on file size to handle large PDFs"""
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        # Adaptive chunking based on file size
        if file_size_mb > 50:  # Large PDF (400+ pages)
            return RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        elif file_size_mb > 20:  # Medium PDF (200+ pages)
            return RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
        else:  # Small files
            return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    except:
        # Default to safe chunking
        return RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

def get_embeddings():
    """Get embeddings with offline support"""
    try:
        return HuggingFaceBgeEmbeddings(
            model_name=EMBEDDING_MODEL, 
            model_kwargs={"device": "cpu"},
            cache_folder="./embeddings_cache",
            # Add these for offline mode
            show_progress=True,
            encode_kwargs={"normalize_embeddings": True}
        )
    except Exception as e:
        print(f"⚠️  HuggingFace download failed: {e}")
        print("🔧 Using fallback local embeddings...")
        
        # Fallback: Use a simpler embedding model
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            cache_folder="./embeddings_cache"
        )

def load_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    loaders = {
        ".pdf":  PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt":  lambda p: TextLoader(p, encoding="utf-8"),
        ".pptx": UnstructuredPowerPointLoader
    }
    if ext not in loaders:
        raise ValueError(f"Unsupported file type: {ext}")
    return loaders[ext](file_path).load()

def build_vector_store(file_path: str) -> Chroma:
    """Build vector store with batched embeddings for large files"""
    print(f"Building vector store for {os.path.basename(file_path)}...")
    
    splitter = get_splitter_for_file(file_path)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Using chunk size: {splitter._chunk_size}")
    
    docs = load_document(file_path)
    print(f"Loaded {len(docs)} pages/documents")
    
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")
    
    embeddings = get_embeddings()
    
    # Batch embedding to avoid timeout/memory issues
    batch_size = 50  # Process 50 chunks at a time
    all_ids = []
    
    print(f"Processing {len(chunks)} chunks in batches of {batch_size}...")
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(chunks) + batch_size - 1) // batch_size
        
        print(f"  Batch {batch_num}/{total_batches}: Embedding {len(batch)} chunks...")
        
        try:
            if i == 0:
                # First batch: create the vector store
                vector_store = Chroma.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    collection_name=COLLECTION_NAME,
                    persist_directory=CHROMA_EXT
                )
            else:
                # Subsequent batches: add to existing
                vector_store.add_documents(batch)
            
            print(f"  ✅ Batch {batch_num} completed")
            
        except Exception as e:
            print(f"  ❌ Batch {batch_num} failed: {str(e)}")
            print(f"  Retrying batch {batch_num}...")
            try:
                if i == 0:
                    vector_store = Chroma.from_documents(
                        documents=batch,
                        embedding=embeddings,
                        collection_name=COLLECTION_NAME,
                        persist_directory=CHROMA_EXT
                    )
                else:
                    vector_store.add_documents(batch)
                print(f"  ✅ Batch {batch_num} succeeded on retry")
            except Exception as retry_error:
                print(f"  ❌ Batch {batch_num} failed on retry: {str(retry_error)}")
                raise
    
    print(f"✅ Vector store built successfully with {len(chunks)} chunks")
    return vector_store

def load_vector_store() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_EXT
    )

def get_retriever(vector_store: Chroma, k: int = 4):
    return vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k})