from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
# from dotenv import load_dotenv
import os

class ChromaDatabase():
    def __init__(self):
        # load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        # self.__GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.__GOOGLE_API_KEY = 'AIzaSyCIRPP0PhNPAR4JNiHxad-vOk6jk7JhCBM'

        self.__model_embedding = 'models/embedding-001'
        self.__collection_name = 'my_collection'
        self.__persist_directory = './chroma'

        self.__first_text = '''Kamu adalah ahli tanaman dan juga teman saya.'''

        self.__embedding = GoogleGenerativeAIEmbeddings(
            google_api_key=self.__GOOGLE_API_KEY,
            model=self.__model_embedding
        )

        self.__vectorstore = Chroma(
            collection_name=self.__collection_name,
            embedding_function=self.__embedding,
            persist_directory=self.__persist_directory
        )

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
