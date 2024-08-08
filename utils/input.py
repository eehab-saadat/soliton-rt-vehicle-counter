from utils.onlycams import list_hot_cameras_on_my_device
import streamlit as st
from tempfile import NamedTemporaryFile
from utils.dialogBox import showDialogBox
from classes.new_model import MODEL
from classes.inference import INSTANCE
from ultralytics import YOLO
from pandas import DataFrame

@st.cache_resource
def load_instance():
    return INSTANCE()

#TODO: remove this function, only here for testing
def removeItem(lst, indx: int = 0):
    lst.pop(indx)
    return lst

# function to load model and add to the instance
def add_model_to_instance(source: str, weights: str = "weights/final.pt"):
    model = MODEL()
    instance: INSTANCE = load_instance()
    model.mount(YOLO("weights/final.pt"))
    instance.add(model, source)

@st.fragment
def update_model_status_table():
    # TODO: insert a tabele with list of running threds and buttons to close those camera threads
    
    # creating dataframe
    sources = load_instance().get_active_sources
    data_df = DataFrame(
    {
        "Active Sources": sources,
        "Select": [False for source in sources],
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


def handle_camera_stream() -> None:
    all_cams = list_hot_cameras_on_my_device()
    st.session_state.model_mounted = True

def on_upload(model, linear_points: list) -> None:
    if st.session_state.get("uploaded_file") is not None: # if a file is uploaded
        video_file = st.session_state.uploaded_file
        instance = load_instance()
        # create a temporary copy of the uploaded file in storage folder
        with NamedTemporaryFile(delete=False, suffix=video_file.name.split(".")[-1]) as temp:
            temp.write(video_file.read())
            add_model_to_instance(temp.name)
        
    else:
        # TODO: show error message popup
        showDialogBox(heading="Upload Error", 
                      message="File not uploaded properly. file not present, incompatible format or file size > 200mb.")
        
def handle_ip_stream(model, source: str, toSkip: int, linear_points: list) -> None:
    model.count(source=source, skip=1, region_points=linear_points)
    #TODO: add error handling for invalid IP addresses
    pass