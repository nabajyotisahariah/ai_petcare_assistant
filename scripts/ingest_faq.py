import os
import logging
from pathlib import Path
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.config import settings

logger = logging.getLogger(__name__)

def ingest_faq_docs():
    faq_dir = Path(settings.faq_dir)
    if not faq_dir.exists():
        logger.warning(f"FAQ directory {faq_dir} does not exist.")
        return

    logger.info("Loading documents...")
    # Supports loading txt files
    loader = DirectoryLoader(str(faq_dir), glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        logger.warning("No documents found to ingest.")
        return

    logger.info(f"Loaded {len(documents)} documents. Chunking...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks.")

    logger.info("Generating embeddings and building vector store (FAISS)...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.openai_api_key
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save locally
    save_path = Path(settings.data_dir) / "faiss_index"
    vectorstore.save_local(str(save_path))
    logger.info(f"Vector store saved to {save_path}")

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    from dotenv import load_dotenv
    load_dotenv()
    ingest_faq_docs()
