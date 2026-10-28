import os

from abc import ABC, abstractmethod

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings


class BaseModelFactory(ABC):

    @abstractmethod
    def generate_factory(self):
        pass

    def api_key(self):
        return os.environ.get("DASHSCOPE_API_KEY", "").strip()


class ChatModelFactory(BaseModelFactory):
    def generate_factory(self):
        return ChatTongyi(model="qwen3.7-max", api_key=self.api_key())

class EmbeddingModelFactory(BaseModelFactory):
    def generate_factory(self):
        return DashScopeEmbeddings(model="text-embedding-v4", dashscope_api_key=self.api_key())


embedding_model = EmbeddingModelFactory().generate_factory()



