from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from chromadb import HttpClient
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

class ChromaDatabase():
    def __init__(self):
        self.__GOOGLE_API_KEY = 'AIzaSyCIRPP0PhNPAR4JNiHxad-vOk6jk7JhCBM'

        self.__model_embedding = 'models/embedding-001'
        self.__collection_name = 'my_collection'

        self.__embedding = GoogleGenerativeAIEmbeddings(
            google_api_key=self.__GOOGLE_API_KEY,
            model=self.__model_embedding
        )

        self.__chroma_host = 'coherent-classic-platypus.ngrok-free.app'  
        self.__chroma_port = 443
        self.__use_ssl = True

        self.__client = HttpClient(
            host=self.__chroma_host,
            port=self.__chroma_port,
            ssl=self.__use_ssl
        )

        self.__vectorstore = Chroma(
            client=self.__client,
            collection_name=self.__collection_name,
            embedding_function=self.__embedding
        )

        self.__first_text = '''Kamu adalah ahli tanaman dan juga teman saya.'''
        self.__insert_first_text_to_chroma()

        self.retriever = self.__vectorstore.as_retriever()

    def __insert_first_text_to_chroma(self):
        if len(self.__vectorstore.get()['documents']) == 0:
            splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
            docs = splitter.create_documents([self.__first_text])
            self.__vectorstore.add_documents(docs)

    def insert_qa_to_chroma(self, answer, question):
        content = f"Q: {question}\nA: {answer}"
        document = Document(page_content=content)
        self.__vectorstore.add_documents([document])
