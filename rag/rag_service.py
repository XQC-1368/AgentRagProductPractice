from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import ChatModelFactory
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_prompt_template


class RagSummaryService:
    def __init__(self):
        self.model = ChatModelFactory().generate_factory()
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.summarize_template = PromptTemplate.from_template(self.load_summarize_prompts())
        self.chain = self.generate_chain()

    def generate_chain(self):
        return self.summarize_template | self.model | StrOutputParser()

    def retrieve_docs(self, question) -> list[Document]:
        return self.retriever.invoke(question)

    def get_summary(self, question):
        docs = self.retrieve_docs(question)
        context = ""
        for doc in docs:
            context += doc.page_content
            context += "\n"
        return self.chain.invoke({"input": question, "context": context})

    def load_summarize_prompts(self):
        return load_prompt_template("rag_summary_prompt.txt")


if __name__ == "__main__":
    service = RagSummaryService()
    print(service.get_summary("滤芯多久更换一次？"))
