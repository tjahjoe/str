# import streamlit as st
# from io import StringIO
# from model_genai import ModelGenai

# class ChatPage:
#     def __init__(self):
#         self.__model = ModelGenai()

#     # @st.cache_resource
#     # def __load_model(_self):
#     #     return ModelGenai()

#     # @st.cache_resource
#     # def __load_chroma(_self):
#     #     return ChromaDatabase()

#     def show(self):
#         st.title('Asisten Ahli Tanaman 🌿')
#         st.markdown('Tanyakan apa saja tentang tanaman. Aku tidak bisa mengingat pertanyaan sebelumnya.')

#         question = st.text_input('Pertanyaan Anda:')

#         if st.button('Tanya') and question.strip():
#             self.__handle_question(question)
#         else:
#             st.info("Masukkan pertanyaan lalu klik tombol 'Tanya'.")

#     def __handle_question(self, question):
#         with st.spinner('Menjawab...'):
#             try:
#                 full_answer = StringIO()
#                 answer_stream = self.__model.chain.stream({'input': question})

#                 response_container = st.empty()
#                 output = ''

#                 for chunk in answer_stream:
#                     content = getattr(chunk, 'content', str(chunk))
#                     output += content
#                     response_container.markdown(output + '▌') 

#                 response_container.markdown(output) 
#                 st.success('✅ Jawaban disimpan ke database.')
#             except Exception as e:
#                 st.error('❌ Terjadi kesalahan. Mungkin kuota API habis.', e)


import streamlit as st
from model_genai import ModelGenai
from chroma_database import ChromaDatabase

class ChatPage:
    def __init__(self):
        self.__model = ModelGenai()
        self.__chroma_database = ChromaDatabase()

    # @st.cache_resource
    # def __load_model(_self):
    #     return ModelGenai()

    # @st.cache_resource
    # def __load_chroma(_self):
    #     return ChromaDatabase()

    def show(self):
        st.title('Asisten Ahli Tanaman 🌿')
        st.markdown('Tanyakan apa saja tentang tanaman. Untuk pertanyaan non-tanaman akan ditolak secara sopan.')

        question = st.text_input('Pertanyaan Anda:')

        if st.button('Tanya') and question.strip():
            self.__handle_question(question)
        else:
            st.info("Masukkan pertanyaan lalu klik tombol 'Tanya'.")

    def __handle_question(self, question):
        with st.spinner('Menjawab...'):
            try:
                answer_stream = self.__model.chain.stream({'question': question})

                response_container = st.empty()
                output = ''

                for chunk in answer_stream:
                    content = getattr(chunk, 'content', str(chunk))
                    output += content
                    response_container.markdown(output + '▌') 

                response_container.markdown(output) 

                self.__chroma_database.insert_qa_to_chroma(output, question)
                st.success('✅ Jawaban disimpan ke database.')
            except Exception as e:
                st.error('❌ Terjadi kesalahan. Mungkin kuota API habis.')


