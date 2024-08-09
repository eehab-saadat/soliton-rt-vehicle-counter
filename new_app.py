# imports
import streamlit as st
from datetime import datetime
from utils.stats import render_statistics
from components.main_pane import display_option_menu
from components.active_camera_table import update_model_status_table
from utils.input import load_instance
from classes.inference import kill_dead_threads

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
    print("\n", st.session_state.sources, "\n")

    if st.session_state.active_cams_present:
        st.session_state.main_pane_cols = 2
    else:
        st.session_state.main_pane_cols = 1

    # title of page
    st.markdown('''<h1 style='text-align: center; color: white; font-style: italic; font-size: 56px; margin:0'>
                    🎁 Autoistics
                </h1>
                <h3 style='text-align: center; color: white; font-style: italic; font-size: 24px; margin:0'>
                    Specially Abled Vehicle Counter
                </h3>
                <br>
                ''', unsafe_allow_html=True)
    
    # setting width of sidebar
    # st.markdown(
    # """
    # <style>
    #     section[data-testid="stSidebar"] {
    #         width: 1000px !important;
    #     }
    # </style>
    # """,
    # unsafe_allow_html=True,
    # )

    st.session_state.main_pane = st.columns([2, 1] if st.session_state.main_pane_cols == 2 else st.session_state.main_pane_cols, 
                                            gap="large",
                                            vertical_alignment="top")


    if "instance" not in st.session_state:
        st.session_state.instance = load_instance()

    # display options menu
    display_option_menu()

    # creating running cameras summary in table here
    if st.session_state.active_cams_present:
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