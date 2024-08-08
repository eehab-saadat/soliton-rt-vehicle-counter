# displaying control panel
import streamlit as st
from streamlit_option_menu import option_menu
from utils.input import on_upload, handle_camera_stream, handle_ip_stream
from utils.onlycams import list_hot_cameras_on_my_device
def display_option_menu():
    with st.session_state.main_pane[0]:
        # heading
        st.header("Control Panel")
        # option menu
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
             IP_address = st.session_state.input_option_bucket.text_input("Enter IP Address", "")
             with st.session_state.start_button:
                st.session_state.run_stream_button = st.button("Start Streaming", 
                                            help="Run the model inference and start counting vehicles from netwrook camera input",
                                            key="run_ip_cam_btn",
                                            on_click=handle_ip_stream,
                                            args=(IP_address,))

        elif st.session_state.selected == "Use Camera":
            # display all available web cams in dropdown
            all_cams = list_hot_cameras_on_my_device()
            st.session_state.selected_cam =  st.session_state.input_option_bucket.selectbox(label="Select camera from the list below",
                                                        options=list(all_cams.keys()))
            with st.session_state.start_button:
                st.session_state.run_cam_button = st.button("Open Camera", 
                                                            help="Run the model inference and start counting vehicles from selected camera input",
                                                            key="run_cam_btn",
                                                            on_click=handle_camera_stream)