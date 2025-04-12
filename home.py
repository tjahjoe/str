import streamlit as st
import cv2
import time
from datetime import datetime
from requests import get
import requests
import numpy as np
from ultralytics import YOLO

class HomePage:
    def __init__(self):
        if 'is_streaming' not in st.session_state:
            st.session_state['is_streaming'] = False
        if 'last_hallo_time' not in st.session_state:
            st.session_state['last_hallo_time'] = time.time()

        self.__model_file = 'best.pt'
        self.__model = YOLO(self.__model_file)
        self.__url = ""  # Initialize URL

    def show(self):
        st.title('Home Overview')
        st.write('Welcome to the main Home')
        col1, col2 = st.columns(2)
        self.__url = st.text_input('Masukkan URL Gambar:', key="image_url_input")

        with col2:
            self._control_streaming()

        with col1:
            self.stream_placeholder = st.empty()
            self.hallo_placeholder = st.empty()
            self.data_placeholder = st.empty()
            self._handle_display()

    def _control_streaming(self):
        if st.button('Start'):
            st.session_state['is_streaming'] = True
        if st.button('Stop'):
            st.session_state['is_streaming'] = False

    def _handle_display(self):
        if st.session_state['is_streaming'] and self.__url != '':
            self._process_url_image(self.__url)
        else:
            st.session_state['is_streaming'] = False

    def _process_url_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            image_bytes = np.asarray(bytearray(response.raw.read()), dtype=np.uint8)
            frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                results = self.__model(frame, verbose=False, conf=0.5)
                detected_frame = results[0].plot()
                self.stream_placeholder.image(detected_frame, channels='RGB')
                # self._update_info()
            else:
                st.error("Gagal membaca gambar dari URL.")

        except requests.exceptions.RequestException as e:
            st.error(f"Terjadi kesalahan saat mengambil gambar dari URL: {e}")
        except Exception as e:
            st.error(f"Terjadi kesalahan tak terduga: {e}")

    # def _update_info(self):
    #     now = time.time()
    #     if now - st.session_state['last_hallo_time'] >= 1:
    #         try:
    #             server_time = get(url='https://indodax.com//api/server_time').json()['server_time']
    #             self.data_placeholder.write(server_time)
    #             self.hallo_placeholder.write(f'hallo - {datetime.now().strftime("%H:%M:%S")}')
    #             st.session_state['last_hallo_time'] = now
    #         except Exception as e:
    #             self.data_placeholder.error(f"Error fetching server time: {e}")
