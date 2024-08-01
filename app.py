# imports
import os
import streamlit as st
import cv2
from classes.model import MODEL
from ultralytics import YOLO
from utils import background_setter

video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"

def main(_args):
    # load the video object
    frame_bucket = st.empty()

    if "frame_bucket" not in st.session_state:
        st.session_state.frame_bucket = frame_bucket
    
    st.write("Video is playing")

    # running model inference
    model = MODEL()
    model.mount(YOLO('weights/final.pt'))
    # region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
    linear_points = [(500, 450), (500, 1300)]
    model.count("samples/sample.mp4", 1, linear_points)

    ## page routing
    page1 = st.Page("classes/model.py")
    router = st.navigation(pages=[page1])
    router.run()

if __name__ == "__main__":
    main(None)