# imports
import os
import streamlit as st
import cv2
from utils import background_setter

video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"

def main(_args):
    # load the video object
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        st.error("Error opening video stream or file")
    frame_bucket = st.empty()
    # open video
    background_setter.set_png_as_page_bg("assets/joker_bkg.png")
    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame_bucket.image(frame, channels="RGB")
    
    cap.release()

    # page routing
    page1 = st.Page("heading1.py")
    page2 = st.Page("heading2.py")
    router = st.navigation(pages=[page1, page2])
    router.run()

if __name__ == "__main__":
    main(None)