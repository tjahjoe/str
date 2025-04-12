import streamlit as st
from model_genai import ModelGenai

class ChatPage:
    def __init__(self):
        self.__model = ModelGenai()

        if 'unsent_question' not in st.session_state:
            st.session_state['unsent_question'] = ''

    def show(self):
        st.title('Asisten Ahli Tanaman 🌿')
        st.markdown('Tanyakan apa saja tentang tanaman. Aku tidak bisa mengingat pertanyaan sebelumnya.')

        question = st.text_input('Pertanyaan Anda:', value=st.session_state['unsent_question'], key='question_input')

        st.session_state['unsent_question'] = question

        if st.button('Tanya') and question.strip():
            self.__handle_question(question)
        else:
            st.info("Masukkan pertanyaan lalu klik tombol 'Tanya'.")

    def __handle_question(self, question):
        with st.spinner('Menjawab...'):
            try:
                st.session_state['unsent_question'] = ''

                answer_stream = self.__model.chain.stream({'input': question})
                response_container = st.empty()
                output = ''

                for chunk in answer_stream:
                    content = getattr(chunk, 'content', str(chunk))
                    output += content
                    response_container.markdown(output + '▌')

                response_container.markdown(output)
                st.success('✅ Jawaban disimpan ke database.')
            except Exception as e:
                st.error('❌ Terjadi kesalahan. Mungkin kuota API habis.')
                st.exception(e)
