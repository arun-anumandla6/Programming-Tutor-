import os
import argparse

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from embeddings import embedding_function


def load_documents(data_dir):
    documents = []

    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".pdf"):
                path = os.path.join(root, file)
                loader = PyPDFLoader(path)
                docs = loader.load()
                documents.extend(docs)

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def create_vector_db(chunks, persist_directory, collection_name):

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory,
        collection_name=collection_name
    )

    db.persist()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--type", required=True)

    args = parser.parse_args()

    data_dir = args.data_dir
    language = args.language.lower()

    COLLECTIONS = {
        "python": "python_index",
        "java": "java_index",
        "go": "go_index"
    }

    print("Loading documents...")
    documents = load_documents(data_dir)

    print("Splitting documents...")
    chunks = split_documents(documents)

    print("Creating vector database...")

    create_vector_db(
        chunks,
        persist_directory="./chroma_db",
        collection_name=COLLECTIONS[language]
    )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()