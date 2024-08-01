# imports
import streamlit as st
from classes.model import MODEL
from ultralytics import YOLO
from utils.background_setter import set_png_as_page_bg
from streamlit_option_menu import option_menu
import cv2

# Mounting model
video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"
model = MODEL()
model.mount(YOLO('weights/final.pt'))
# region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
linear_points = [(500, 450), (500, 1300)]

def main(_args):
    
    ### Method Definitions ###
    def on_upload() -> None:
        if st.session_state.get("uploaded_file") is not None: # if a file is uploaded
            video_file = st.session_state.uploaded_file
            print(video_file)
            
            
        else:
            print("file not uploaed")
    # page configurations
    config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗"
    )
    st.header("Vehicle Detection")

    # Option Menu
    selected = option_menu("Select Video", 
                            ["Upload", "With IP Address", "Use Webcam"],
                            icons=["upload", "hdd-network", "camera"],
                            orientation="horizontal")

    # frame_bucket.subheader("Link your vidoe upload method from Side Menu and clcik \"RUN\"")

    if selected == "Upload":
        uploaded_file = st.file_uploader(label="Upload Video:hot_pepper:", 
                        type=["mp4", "avi", "mov", "mkv"], 
                        help="Upload a video file. Allowed formats: mp4, avi, mov, mkv",
                        accept_multiple_files=False)
        upload_button = st.button(label="Upload", 
                            key="upload_btn", 
                            help="Run the model inference and start counting vehicles",
                            on_click=on_upload)
        # add to session dict
        st.session_state.uploaded_file = uploaded_file
        
    if selected == "With IP Address":
        st.write("Enter your IP Address")
    if selected == "Use Webcam":
        st.write("Use your webcam")

    ## page routing
    # page1 = st.Page("classes/model.py")
    # router = st.navigation(pages=[page1])
    # router.run()

if __name__ == "__main__":
    main(None)