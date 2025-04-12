from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from server.chroma_database import ChromaDatabase
# from dotenv import load_dotenv
from langchain_core.runnables import RunnableMap, RunnablePassthrough
import os

class ModelGenai():
    def __init__(self):
        # load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        # self.__GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        self.__GOOGLE_API_KEY = 'AIzaSyCIRPP0PhNPAR4JNiHxad-vOk6jk7JhCBM'
        self.__model = 'gemini-1.5-pro'

        self.__chroma_database = ChromaDatabase()
        self.__retriever = self.__chroma_database.retriever

        self.__system_template = 'Kamu adalah asisten ahli tanaman dan juga teman saya.'
        self.__human_template = 'Gunakan konteks berikut untuk menjawab:\n\n{context}\n\nPertanyaan: {question}'
        
        self.__prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.__system_template),
            HumanMessagePromptTemplate.from_template(self.__human_template)
        ])

        self.__llm = ChatGoogleGenerativeAI(
            api_key=self.__GOOGLE_API_KEY,
            model=self.__model,
            streaming=True
        )

        self.chain = (
            RunnableMap({
                "context": lambda x: self.__format_docs(self.__retriever.invoke(x["question"])),
                "question": RunnablePassthrough()
            })
            | self.__prompt_template
            | self.__llm
        )

    def __format_docs(self, docs):
        return "\n\n".join([doc.page_content for doc in docs])
