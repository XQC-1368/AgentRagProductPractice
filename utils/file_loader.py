import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def pdf_loader(path)->list[Document]:
    loader=PyPDFLoader(path)
    return loader.load()
def txt_loader(path)->list[Document]:
    loader=TextLoader(path, encoding="utf-8")
    return loader.load()
    
def list_docs_name(path):
    file_collection=[]
    files=os.listdir(path)
    for file in files:
        file_collection.append(os.path.join(path,file))
    return file_collection


if __name__ == "__main__":
    documents = list_docs_name("./knowledge_database")
    print("files:", documents)
    for doc in documents:
        if doc.endswith(".txt"):
            docs = txt_loader(doc)
        elif doc.endswith(".pdf"):
            docs = pdf_loader(doc)
        else:
            continue
        print(doc, "->", len(docs), "documents")
        print(docs[0].page_content[:60])
        
