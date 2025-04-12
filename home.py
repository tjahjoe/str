import streamlit as st
import cv2
import time
import numpy as np
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
            uploaded_file = st.file_uploader("Unggah Foto", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
                if image is not None:
                    frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
                    results = self.__model(frame, verbose=False, conf=0.5)
                    detected_frame = results[0].plot()
                    self.stream_placeholder.image(detected_frame, channels='BGR')
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
