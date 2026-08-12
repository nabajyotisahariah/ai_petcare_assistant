import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.config import settings

def ingest_faq_docs():
    faq_dir = Path(settings.faq_dir)
    if not faq_dir.exists():
        print(f"FAQ directory {faq_dir} does not exist.")
        return

    print("Loading documents...")
    # Supports loading txt files
    loader = DirectoryLoader(str(faq_dir), glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("No documents found to ingest.")
        return

    print(f"Loaded {len(documents)} documents. Chunking...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings and building vector store (FAISS)...")
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save locally
    save_path = Path(settings.data_dir) / "faiss_index"
    vectorstore.save_local(str(save_path))
    print(f"Vector store saved to {save_path}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    ingest_faq_docs()