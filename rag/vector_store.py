
import os
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model.factory import embedding_model
from utils import file_loader
from langchain_core.vectorstores import VectorStoreRetriever

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class VectorStoreService:
    def __init__(self) :
        self.vector_store: Chroma = Chroma(
            persist_directory=os.path.join(BASE_DIR, "chroma_db"),
            embedding_function=embedding_model,
        )
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=200, 
                                                       chunk_overlap=20,
                                                       separators=["\n","\n\n",","," ",".","。","!","?"]
                                                       )
        
    def get_file_md5_hex(self, file_path):
        import hashlib
        with open(file_path, "rb") as f:
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            return hash_code

    def check_md5(self, md5_hex):
        md5_hex_path = os.path.join(BASE_DIR, "md5_hex.txt")
        if os.path.exists(md5_hex_path):
            with open(md5_hex_path, "r") as f:
                md5_hex_list = f.readlines()
                if md5_hex in [line.strip() for line in md5_hex_list]:
                    return True
        return False

    def save_md5(self, md5_hex):
        with open(os.path.join(BASE_DIR, "md5_hex.txt"), "a") as f:
            f.write(md5_hex + "\n")

    def get_retriever(self) -> VectorStoreRetriever:
        return self.vector_store.as_retriever(search_kwargs={"k": 3})
        
    def load_document(self):
        documents = file_loader.list_docs_name(os.path.join(BASE_DIR, "knowledge_database"))
        for doc in documents:
            temp_md5 = self.get_file_md5_hex(doc)
            if self.check_md5(temp_md5):
                continue
            else:
                #使用txtloader或者pdfloader加载文件
                if doc.endswith(".txt"):
                    docs = file_loader.txt_loader(doc)
                elif doc.endswith(".pdf"):
                    docs = file_loader.pdf_loader(doc)
                else:
                    continue
            #使用切割器切分文本
            docs = self.splitter.split_documents(docs)
            self.vector_store.add_documents(docs)
            #保存md5
            self.save_md5(temp_md5)


if __name__ == "__main__":
    service = VectorStoreService()  # 创建向量库服务实例，连接本地 chroma_db 数据库
    service.load_document()  # 加载知识库文档：切分、向量化并写入向量库（已处理过的文件会跳过）
    print("chunks:", service.vector_store._collection.count())  # 打印向量库中切分块的总数，验证文档是否入库成功
    results = service.get_retriever().invoke("滤芯多久更换一次")  # 用检索器查询该问题，返回最相似的 3 个文档块
    for i, doc in enumerate(results, 1):  # 遍历检索结果，序号从 1 开始
        print(f"--- TOP{i} ---")  # 打印当前结果的排名标题
        print(doc.page_content)  # 打印文档块内容，检查检索结果是否相关
                
                
