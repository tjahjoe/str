import streamlit as st
import cv2
import requests
import numpy as np
import base64
import streamlit.components.v1 as components
from datetime import datetime
from ultralytics import YOLO

class DetectionPage:
    def __init__(self):
        if 'is_streaming' not in st.session_state:
            st.session_state['is_streaming'] = False
        if 'last_image' not in st.session_state:
            st.session_state['last_image'] = None

        self.__model_file = 'best.pt'
        self.__model = YOLO(self.__model_file)
        self.__url = 'https://api-smart-pot.vercel.app/get/image' 

    def show(self):
        st.title('Deteksi Objek 🔍')
        st.markdown('Selamat datang di halaman deteksi objek! 👀')
        st.markdown('Tekan tombol "Ambil Gambar" untuk melakukan deteksi.')
        col1, col2 = st.columns(2)

        with col2:
            self._control_streaming()

        with col1:
            self.stream_placeholder = st.empty()
            self.hallo_placeholder = st.empty()
            self.data_placeholder = st.empty()
            self._handle_display()

    def _control_streaming(self):
        if st.button('Ambil Gambar 📸'):
            st.session_state['is_streaming'] = True
            st.session_state['last_image'] = None
        if st.button('Unduh 💾'):
            self._download_button()
        if st.button('Berhenti 🛑'):
            st.session_state['is_streaming'] = False
            st.session_state['last_image'] = None

    def _handle_display(self):
        if st.session_state['is_streaming'] and st.session_state['last_image'] is not None:
            self.stream_placeholder.image(st.session_state['last_image'], channels='RGB')
        elif st.session_state['is_streaming']:
            self._process_url_image(self.__url)

    def _process_url_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            image_bytes = np.asarray(bytearray(response.raw.read()), dtype=np.uint8)

            st.session_state['last_image'] = image_bytes

            frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                results = self.__model(frame, verbose=False, conf=0.5)
                detected_frame = results[0].plot()
                st.session_state['last_image'] = detected_frame

                self.stream_placeholder.image(st.session_state['last_image'], channels='RGB')
            else:
                st.error("Gagal membaca gambar dari URL 😞.")
                st.session_state['is_streaming'] = False
                
        except Exception as e:
            st.error(f"Terjadi kesalahan tak terduga 💥: {e}")
            st.session_state['is_streaming'] = False
    
    def _download_button(self):
        if st.session_state['last_image'] is not None:
            rgb_image = cv2.cvtColor(st.session_state['last_image'], cv2.COLOR_RGB2BGR)
            success, buffer = cv2.imencode('.jpg', rgb_image)

            if success:
                b64 = base64.b64encode(buffer).decode()
                filename = f"detected_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                href = f'''
                        {st.success("🎉 Gambar berhasil diunduh!")
}
                        <a href="data:file/jpg;base64,{b64}" download="{filename}" id="download-link"></a>
                        
                        <script>
                            document.getElementById("download-link").click()
                        </script>
                        '''
                components.html(href, height=0, width=0)
            else:
                st.error("Gagal mengkodekan gambar untuk diunduh.")
        else:
            st.warning("Tidak ada gambar yang terdeteksi untuk diunduh.")




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
