# imports
import streamlit as st
# from classes.model import MODEL
# from ultralytics import YOLO
from utils.background_setter import set_png_as_page_bg
from streamlit_option_menu import option_menu
from utils.onlycams import list_hot_cameras_on_my_device
from utils.upload import on_upload
from utils.camera import handle_camera_stream
from utils.main_layout import handle_show_vid
from datetime import datetime
from utils.stats import render_statistics
from pandas import read_csv, DataFrame

## Mounting model
# video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"
# model = MODEL()
# model.mount(YOLO('weights/final.pt'))
# region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
linear_points = [(500, 450), (500, 1300)]

def main(_args):

    # page configurations
    initial_layout = "centered"
    config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗",
        layout=st.session_state.current_layout if "current_layout" in st.session_state else initial_layout
    )

    if "current_layout" not in st.session_state:
        st.session_state.current_layout = initial_layout

    # page layout structures / containers
    if "main_pane" not in st.session_state:
        st.session_state.main_pane_cols = 1
    else:
        if st.session_state.display_checkbox:
            st.session_state.main_pane_cols = 2
        else:
            st.session_state.main_pane_cols = 1

    main_pane = st.columns(st.session_state.main_pane_cols, vertical_alignment="top", gap='small')
    st.session_state.main_pane = main_pane

    with st.session_state.main_pane[0]:

        header_row = st.columns(spec=[4,1], gap="small", vertical_alignment="bottom")
        with header_row[0]:
            st.header("Vehicle Detection")
        with header_row[1]:
            display_checkbox = st.checkbox(label="Show Video", key="show_vid", on_change=handle_show_vid)
            st.session_state.display_checkbox = display_checkbox
        
        # Option Menu
        menu_options = ["Upload", "With IP Address", "Use Camera"]
        selected = option_menu("Select Video", 
                                options=menu_options,
                                icons=["upload", "hdd-network", "camera"],
                                orientation="horizontal",
                                menu_icon="record-btn")
        if "option_menu" not in st.session_state:
            st.session_state.option_menu = selected

        # empty container for input option
        st.session_state.input_option_bucket = st.empty()
        start_button, download_button = st.columns([3, 1], gap="small")

        # download button
        # TODO: manage 
        with download_button:
            st.download_button(label="Download Report", 
                                data='counts.csv',
                                file_name=f"report_{datetime.now()}",
                                mime="text/csv",
                                help="Download the vehicle count report in CSV format")
            
        if selected == "Upload":
            uploaded_file =  st.session_state.input_option_bucket.file_uploader(label="Upload Video:hot_pepper:", 
                            type=["mp4", "avi", "mov", "mkv"], 
                            help="Upload a video file. Allowed formats: mp4, avi, mov, mkv",
                            accept_multiple_files=False)
            with start_button:
                upload_button = st.button(label="Upload", 
                                    key="upload_btn", 
                                    help="Run the model inference and start counting vehicles",
                                    on_click=on_upload)
            # add to session dict
            st.session_state.input_option_bucket.uploaded_file = uploaded_file
            
        if selected == "With IP Address":
            st.session_state.input_option_bucket.IP_address = st.session_state.input_option_bucket.text_input("Enter IP Address", "")
            with start_button:
                run_stream_button = st.button("Start Streaming", 
                                            help="Run the model inference and start counting vehicles from netwrook camera input",
                                            key="run_ip_cam_btn")
                                            # on_click=lambda: model.count("http://" + IP_address, 1, linear_points)

        if selected == "Use Camera":
            # display all available web cams in dropdown
            all_cams = list_hot_cameras_on_my_device()
            st.session_state.input_option_bucket.selected_cam =  st.session_state.input_option_bucket.selectbox(label="Select camera from the list below",
                                                        options=list(all_cams.keys()))
            with start_button:
                st.session_state.run_cam_button = st.button("Open Camera", 
                                            help="Run the model inference and start counting vehicles from selected camera input",
                                            key="run_cam_btn",
                                            on_click=handle_camera_stream)
                
    # container declaration for video streaming
    if st.session_state.main_pane_cols == 2:
          with main_pane[1]:
            st.session_state.frame_bucket = st.empty()
            st.session_state.frame_bucket.image(image="assets/placeholder-bg.png")

    # rendering data vidualization
    render_statistics()


    ## page routing
    # page1 = st.Page("classes/model.py")
    # router = st.navigation(pages=[page1])
    # router.run()

if __name__ == "__main__":
    main(None)