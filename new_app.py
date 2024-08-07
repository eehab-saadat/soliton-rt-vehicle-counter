# imports
import streamlit as st
# from classes.new_model import MODEL
# from ultralytics import YOLO
from streamlit_option_menu import option_menu
from utils.onlycams import list_hot_cameras_on_my_device
from utils.input import handle_camera_stream, on_upload, handle_ip_stream, update_model_status_table
from utils.main_layout import handle_show_vid
from datetime import datetime
from utils.stats import render_statistics
from pandas import read_csv, DataFrame
import cv2

from utils.input import removeItem, load_instance

## Mounting model
video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"
region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
linear_points = [(500, 450), (500, 1300)]

def main(_args):

    #st.fragment

    # page configurations
    page_config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # status of model
    if "model_mounted" not in st.session_state:
        st.session_state.model_mounted = False

    # title of page
    st.markdown('''<h1 style='text-align: center; color: white; font-style: italic; font-size: 56px; margin:0'>
                    🎁 Autoistics
                </h1>
                <h3 style='text-align: center; color: white; font-style: italic; font-size: 24px; margin:0'>
                    Specially Abled Vehicle Counter
                </h3>
                <br>
                ''', unsafe_allow_html=True)
    
    # st.sidebar.markdown('''<h2 style='text-align: center; color: white; font-style: italic; font-size: 24px; margin:0'>''')
    # displaying the control panel
    with st.sidebar:
        # heading
        st.header(" Control Panel")
        # option menu
        if "menu_options" not in st.session_state:
            st.session_state.menu_options = ["Upload", "With IP Address", "Use Camera"]
        selected = option_menu("Select Video", 
                                options=st.session_state.menu_options,
                                icons=["upload", "hdd-network", "camera"],
                                orientation="vertical",
                                menu_icon="record-btn")
        
        if "option_menu" not in st.session_state:
            st.session_state.selected = selected

         # empty container for input option
        st.session_state.input_option_bucket = st.empty()
        st.session_state.start_button, st.session_state.download_button = st.columns([1,1], gap="small")

        if st.session_state.selected == "Upload":
            # create and upload file dropbox and opload button
            uploaded_file =  st.session_state.input_option_bucket.file_uploader(label="Upload Video:hot_pepper:", 
                            type=["mp4", "avi", "mov", "mkv"], 
                            help="Upload a video file. Allowed formats: mp4, avi, mov, mkv",
                            accept_multiple_files=False)
            with st.session_state.start_button:
                st.session_state.upload_button = st.button(label="Upload", 
                                                        key="upload_btn", 
                                                        help="Run the model inference and start counting vehicles",
                                                        on_click=on_upload)
            st.session_state.uploaded_file = uploaded_file

        elif st.session_state.selected == "With IP Address":
             st.session_state.input_option_bucket.IP_address = st.session_state.input_option_bucket.text_input("Enter IP Address", "")
             with st.session_state.start_button:
                st.session_state.run_stream_button = st.button("Start Streaming", 
                                            help="Run the model inference and start counting vehicles from netwrook camera input",
                                            key="run_ip_cam_btn")
                                            # on_click=lambda: model.count("http://" + IP_address, 1, linear_points)

        elif st.session_state.selected == "Use Camera":
            # display all available web cams in dropdown
            all_cams = list_hot_cameras_on_my_device()
            st.session_state.input_option_bucket.selected_cam =  st.session_state.input_option_bucket.selectbox(label="Select camera from the list below",
                                                        options=list(all_cams.keys()))
            with st.session_state.start_button:
                st.session_state.run_cam_button = st.button("Open Camera", 
                                                            help="Run the model inference and start counting vehicles from selected camera input",
                                                            key="run_cam_btn",
                                                            on_click=handle_camera_stream,
                                                            disabled=st.session_state.model_mounted)
    if "instance" not in st.session_state:
        st.session_state.instance = load_instance()
    
    st.session_state.model_table = st.empty()

    update_model_status_table()

    # diaplay stats and data visualization
    st.write("## Vehicle Count Statistics")
    try:
        # TODO: make the visualization functions use current date's csv file only
        render_statistics()
    except Exception as e:
        pass

    # downalod button 
    #TODO: change download button to show a dialog box with a file selector and custom downalod option
    with st.session_state.download_button:
        st.download_button(label="Download Report", 
                            data=st.session_state.data_for_visualization.to_csv(index=False),
                            file_name=f"report_{datetime.now().strftime("%y-%m-%d_%H-%M-%S")}.csv",
                            mime="text/csv",
                            help="Download the vehicle count report in CSV format")
    
    # page footer
    st.markdown("""
    <footer style="text-align:center; padding: 0px; background-color: transparent; bottom: 0; width: 100%; color: white;">
        <br>© 2024 Autoistics. All rights reserved. Developed by Eehab and Fayyez with love. ✨
    </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main(None)