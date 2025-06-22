import os
from parser import extract_text_from_pdf, extract_text_from_docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def index_documents(folder_path: str, persist_path: str):
    texts = []

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)

        if file.lower().endswith(".pdf"):
            print(f"PDF: {file}")
            raw_text = extract_text_from_pdf(full_path)
            texts.append(raw_text)

        elif file.lower().endswith(".docx"):
            print(f"DOCX: {file}")
            raw_text = extract_text_from_docx(full_path)
            texts.append(raw_text)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = splitter.create_documents(texts)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(persist_path)

if __name__ == "__main__":
    index_documents(folder_path="data/pdfs", persist_path="vectorstore/faiss_index")
