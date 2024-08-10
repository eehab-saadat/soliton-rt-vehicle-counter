# imports
import streamlit as st
from datetime import datetime
from utils.stats import render_statistics
from components.main_pane import display_option_menu
from components.active_camera_table import update_model_status_table
from utils.input import load_instance
from classes.inference import kill_dead_threads
from components.download_component import file_downloader

## Mounting model
video_path = r"C:\Users\Fayyez.Farrukh\Documents\NPI\Og videos\002.mp4"
region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
linear_points = [(500, 450), (500, 1300)]

def main(_args):

    # page configurations
    page_config = st.set_page_config(
        page_title="Object Counter",
        page_icon="🚗",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # creating dataframe
    instance = load_instance()
    kill_dead_threads(instance.instances) # kill all dead instances if any
    st.session_state.sources = instance.get_active_sources()
    st.session_state.active_cams_present = True if len(st.session_state.sources) > 0 else False

    if st.session_state.active_cams_present:
        st.session_state.main_pane_cols = 2
    else:
        st.session_state.main_pane_cols = 1

    # title of page
    st.markdown('''<h1 style='text-align: center; color: white; font-style: italic; font-size: 56px; margin:0'>
                    🎁 Autoistics
                </h1>
                <br>
                ''', unsafe_allow_html=True)

    st.session_state.main_pane = st.columns([3, 2] if st.session_state.main_pane_cols == 2 else st.session_state.main_pane_cols, 
                                            gap="large",
                                            vertical_alignment="top")


    if "instance" not in st.session_state:
        st.session_state.instance = load_instance()

    # display options menu
    display_option_menu()

    # creating running cameras summary in table here
    if st.session_state.active_cams_present:
        update_model_status_table()

    # downalod button
    with st.session_state.download_button:
        st.button(label="Download Report",
                help="Download the vehicle count report in CSV format and visualise the data",
                on_click=file_downloader,
                use_container_width=True)

    # page footer
    st.markdown("""
    <footer style="text-align:center; padding: 0px; background-color: transparent; bottom: 0; width: 100%; color: white;">
        <br>© 2024 Autoistics. All rights reserved. Developed by Eehab and Fayyez. ✨
    </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main(None)