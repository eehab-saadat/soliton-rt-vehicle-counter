import streamlit as st
from pandas import DataFrame
from utils.input import load_instance

def handle_remove_camera(sources_to_kill: list):
    instance = load_instance()
    for source in sources_to_kill:
        instance.stop(source=source)

def update_model_status_table():
    # TODO: insert a tabele with list of running threds and buttons to close those camera threads
     with st.session_state.main_pane[1]:
            st.header("Active Cameras")
            # adding temporary sources for testing
            data_df = DataFrame({
                "Select": [False for source in st.session_state.sources],
                "Active Sources": st.session_state.sources,
            })
            # creating the editable table with checkboxes
            st.session_state.running_cameras_table = st.data_editor(
                data_df,
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Select",
                        help="Select the active cameras that you want to delete",
                        default=False,
                    )
                },
                disabled=["Active Sources"],
                hide_index=True,
            )

            # remove button to remove the selected cameras
            st.session_state.remove_button = st.button("Remove", 
                                                        key="remove_btn", 
                                                        help="Removes the selected cameras from the active cameras list",
                                                        on_click=handle_remove_camera,
                                                        # TODO: add the list of the selected camera sources to the remove_camera function as args
                                                        args=(st.session_state.running_cameras_table[st.session_state.running_cameras_table["Select"]]["Active Sources"].tolist(),))
            # selected_widgets = myvar[myvar["favorite"]]["widgets"].tolist() 