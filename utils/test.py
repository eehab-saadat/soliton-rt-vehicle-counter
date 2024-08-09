from classes.new_model import MODEL
from cv2 import VideoCapture
import streamlit as st

@st.fragment(run_every=0.1)
def updateFrame():
    frame = st.session_state.model_instance.read()
    if frame is not None:
        st.session_state.frame_bucket.image(frame, channels="BGR")
    else:
        st.session_state.frame_bucket.image(image="assets/placeholder-bg.png")