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

    def handle_reset():
        st.session_state.model_mounted = False
        st.session_state.menu_options = ["Upload", "With IP Address", "Use Camera"]

    # page configurations
    initial_layout = "centered"
    config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗",
        layout=st.session_state.current_layout if "current_layout" in st.session_state else initial_layout
    )

    if "current_layout" not in st.session_state:
        st.session_state.current_layout = initial_layout
    
    if "model_mounted" not in st.session_state:
        st.session_state.model_mounted = False

    # page layout structures / containers
    if "main_pane" not in st.session_state:
        st.session_state.main_pane_cols = 1
    else:
        if st.session_state.display_checkbox:
            st.session_state.main_pane_cols = 2
        else:
            st.session_state.main_pane_cols = 1

    st.markdown('''<h1 style='text-align: center; color: white; font-style: italic; font-size: 56px; margin:0'>
                    🎁 Autoistics
                </h1>
                <h3 style='text-align: center; color: white; font-style: italic; font-size: 24px; margin:0'>
                    Specially Abled Vehicle Counter
                </h3>
                <br>
                ''', unsafe_allow_html=True)

    st.session_state.main_pane = st.columns(st.session_state.main_pane_cols, vertical_alignment="top", gap='small')

    with st.session_state.main_pane[0]:

        header_row = st.columns(spec=[4,1], gap="small", vertical_alignment="center")
        with header_row[0]:
            st.header("Control Panel")
        with header_row[1]:
            display_checkbox = st.checkbox(label="Show Video", key="show_vid", on_change=handle_show_vid)
            st.session_state.display_checkbox = display_checkbox
        
        # Option Menu
        if "menu_options" not in st.session_state:
            st.session_state.menu_options = ["Upload", "With IP Address", "Use Camera"]
        selected = option_menu("Select Video", 
                                options=st.session_state.menu_options,
                                icons=["upload", "hdd-network", "camera"],
                                orientation="horizontal",
                                menu_icon="record-btn")
        if "option_menu" not in st.session_state:
            st.session_state.selected = selected

        # empty container for input option
        st.session_state.input_option_bucket = st.empty()
        st.session_state.start_button, st.session_state.download_button = st.columns([3, 1], gap="small")
    
        if len(st.session_state.menu_options) == 1: # if a model is mounted then show reset button to the user
            st.write("Model inference is running. Press \"Reset\" button to use another video source.")
            st.session_state.start_button, st.session_state.download_button = st.columns([3, 1], gap="small")
            with st.session_state.start_button:
                st.session_state.run_cam_button = st.button("Reset", 
                                                            help="reset the model and start over",
                                                            key="reset_btn",
                                                            on_click=handle_reset)
                
        elif selected == "Upload":
            uploaded_file =  st.session_state.input_option_bucket.file_uploader(label="Upload Video:hot_pepper:", 
                            type=["mp4", "avi", "mov", "mkv"], 
                            help="Upload a video file. Allowed formats: mp4, avi, mov, mkv",
                            accept_multiple_files=False)
            with st.session_state.start_button:
                upload_button = st.button(label="Upload", 
                                    key="upload_btn", 
                                    help="Run the model inference and start counting vehicles",
                                    on_click=on_upload)
            # add to session dict
            st.session_state.uploaded_file = uploaded_file
            
        elif selected == "With IP Address":
            st.session_state.input_option_bucket.IP_address = st.session_state.input_option_bucket.text_input("Enter IP Address", "")
            with st.session_state.start_button:
                run_stream_button = st.button("Start Streaming", 
                                            help="Run the model inference and start counting vehicles from netwrook camera input",
                                            key="run_ip_cam_btn")
                                            # on_click=lambda: model.count("http://" + IP_address, 1, linear_points)

        elif selected == "Use Camera":
            # display all available web cams in dropdown
            all_cams = list_hot_cameras_on_my_device()
            st.session_state.input_option_bucket.selected_cam =  st.session_state.input_option_bucket.selectbox(label="Select camera from the list below",
                                                        options=list(all_cams.keys()))
            with st.session_state.start_button:
                st.session_state.run_cam_button = st.button("Open Camera", 
                                                            help="Run the model inference and start counting vehicles from selected camera input",
                                                            key="run_cam_btn",
                                                            on_click=handle_camera_stream)


    # container declaration for video streaming
    if st.session_state.main_pane_cols == 2:
          with st.session_state.main_pane[1]:
            if "frame_bucket" not in st.session_state:
                st.session_state.frame_bucket_container = st.container()
                st.session_state.frame_bucket = st.session_state.frame_bucket_container.empty()
            if not st.session_state.model_mounted:
                st.session_state.frame_bucket.image(image="assets/placeholder-bg.png")
    
    with st.session_state.main_pane[0]:
        st.write("## Vehicle Count Statistics")

    # rendering data vidualization
    render_statistics()

    
    # download button
    # TODO: manage 
    with st.session_state.download_button:
        st.download_button(label="Download Report", 
                            data=st.session_state.data_for_visualization.to_csv(index=False),
                            file_name=f"report_{datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.csv",
                            mime="text/csv",
                            help="Download the vehicle count report in CSV format")
    
    st.markdown("""
    <footer style="text-align:center; padding: 0px; background-color: transparent; bottom: 0; width: 100%; color: white;">
        <br>© 2024 Autoistics. All rights reserved. Developed by Eehab and Fayyez with love. ✨
    </footer>
    """, unsafe_allow_html=True)


    ## page routing
    # page1 = st.Page("classes/model.py")
    # router = st.navigation(pages=[page1])
    # router.run()

if __name__ == "__main__":
    main(None)