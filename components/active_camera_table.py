import streamlit as st
from pandas import DataFrame
from utils.input import load_instance

def handle_remove_camera():
    pass

def update_model_status_table():
    # TODO: insert a tabele with list of running threds and buttons to close those camera threads
     with st.session_state.main_pane[1]:
            st.header("Active Cameras")
            # adding temporary sources for testing
            data_df = DataFrame({
                "Active Sources": st.session_state.sources,
                "Select": [False for source in st.session_state.sources],
            })
            # creating the editable table with checkboxes
            st.session_state.running_cameras_table = st.data_editor(
                data_df,
                column_config={
                    "favorite": st.column_config.CheckboxColumn(
                        "Your favorite?",
                        help="Select your *favorite* widgets",
                        default=False,
                    )
                },
                disabled=["widgets"],
                hide_index=True,
            )

            # remove button to remove the selected cameras
            st.session_state.remove_button = st.button("Remove", 
                                                        key="remove_btn", 
                                                        help="Removes the selected cameras from the active cameras list",
                                                        on_click=handle_remove_camera,
                                                        # TODO: add the list of the selected camera sources to the remove_camera function as args
                                                        args=())