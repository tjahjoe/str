import streamlit as st
import cv2
import time
from datetime import datetime
from requests import get
from ultralytics import YOLO

class HomePage:
    def __init__(self):
        if 'is_streaming' not in st.session_state:
            st.session_state['is_streaming'] = False
        if 'last_hallo_time' not in st.session_state:
            st.session_state['last_hallo_time'] = time.time()

        self.__model_file = 'best.pt'
        self.__model = YOLO(self.__model_file)

    def show(self):
        st.title('Home Overview')
        st.write('Welcome to the main Home')
        col1, col2 = st.columns(2)
        self.__url = st.text_input('masukkan url:')

        with col2:
            self._control_streaming()

        with col1:
            self.stream_placeholder = st.empty()
            self.hallo_placeholder = st.empty()
            self.data_placeholder = st.empty()
            self._handle_streaming()

    def _control_streaming(self):
        if st.button('Start'):
            st.session_state['is_streaming'] = True
        if st.button('Stop'):
            st.session_state['is_streaming'] = False

    def _handle_streaming(self):
        st.write(st.session_state['is_streaming'])
        if st.session_state['is_streaming'] and self.__url != '':
            cap = cv2.VideoCapture(self.__url)
            try:
                while st.session_state['is_streaming']:
                    success, frame = cap.read()
                    if not success:
                        break

                    frame = cv2.flip(frame, 1)
                    results = self.__model(frame, verbose=False, conf=0.5)
                    frame = results[0].plot()

                    self.stream_placeholder.image(frame, channels='BGR')
                    self._update_info()
            finally:
                cap.release()
                cv2.destroyAllWindows()
        else :
            st.session_state['is_streaming'] = False

    def _update_info(self):
        now = time.time()
        if now - st.session_state['last_hallo_time'] >= 1:
            try:
                server_time = get(url='https://indodax.com//api/server_time').json()['server_time']
                self.data_placeholder.write(server_time)
                self.hallo_placeholder.write(f'hallo - {datetime.now().strftime("%H:%M:%S")}')
                st.session_state['last_hallo_time'] = now
            except Exception as e:
                self.data_placeholder.error(f"Error fetching server time: {e}")
