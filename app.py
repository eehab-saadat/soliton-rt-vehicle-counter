# imports
import streamlit as st
# from classes.model import MODEL
# from ultralytics import YOLO
from utils.background_setter import set_png_as_page_bg
from streamlit_option_menu import option_menu
import cv2
import tempfile

# Mounting model
# video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"
# model = MODEL()
# model.mount(YOLO('weights/final.pt'))
# # region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
# linear_points = [(500, 450), (500, 1300)]

def main(_args):
    
    ### Method Definitions ###
    def on_upload() -> None:
        if st.session_state.get("uploaded_file") is not None: # if a file is uploaded
            video_file = st.session_state.uploaded_file
            # model.count(src=video_file.upload_url)
            # create a temporary copy of the uploaded file in storage folder
            with tempfile.NamedTemporaryFile(delete=False, suffix=video_file.name.split(".")[-1]) as temp:
                temp.write(video_file.read())
                # model.count(temp.name, 1, linear_points)
            
        else:
            # TODO: show error message popup
            st.write("file not uploaed")

    # page configurations
    config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗",
        layout="wide"
    )
    st.header("Vehicle Detection")

    # page layout structures / containers
    main_pane = st.columns(2, vertical_alignment="top", gap='small')
    st.session_state.main_pane = main_pane

    with main_pane[0]:
        # Option Menu
        selected = option_menu("Select Video", 
                                ["Upload", "With IP Address", "Use Webcam"],
                                icons=["upload", "hdd-network", "camera"],
                                orientation="horizontal",
                                menu_icon="record-btn")

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
            IP_address = st.text_input("Enter IP Address", "")
            run_stream_button = st.button("Run", 
                                        help="Run the model inference and start counting vehicles from netwrook camera input",
                                        key="run_btn",
                                        )
            # on_click=lambda: model.count("http://" + IP_address, 1, linear_points)
        if selected == "Use Webcam":
            print("model running")
            # model.count(skip=2, region_points=linear_points)

    st.session_state.frame_bucket = st.empty()
    ## page routing
    # page1 = st.Page("classes/model.py")
    # router = st.navigation(pages=[page1])
    # router.run()

if __name__ == "__main__":
    main(None)