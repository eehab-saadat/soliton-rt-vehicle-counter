from utils.onlycams import list_hot_cameras_on_my_device
from streamlit import session_state, rerun, fragment, container, cache_resource, button, header, write, columns
from tempfile import NamedTemporaryFile
from utils.dialogBox import showDialogBox
from classes.new_model import MODEL
from classes.inference import INSTANCE
from ultralytics import YOLO

@cache_resource
def load_instance():
    return INSTANCE()

#TODO: remove this function, only here for testing
def removeItem(lst, indx: int = 0):
    lst.pop(indx)
    return lst

# function to load model and add to the instance
def add_model_to_instance(source: str, weights: str = "weights/final.pt"):
    model = MODEL()
    model.mount(YOLO("weights/final.pt"))
    instance.add(model, temp.name)

@fragment
def update_model_status_table():
    # TODO: insert a tabele with list of running threds and buttons to close those camera threads
    header("Running Cameras")
    for i, item in enumerate(session_state.instance):
        col1, col2 = columns(2, gap="small")
        with col1:
            write(item)
        with col2:
            if button("❌", key=f"close_btn_{i}"):
                session_state.instance = removeItem(session_state.instance, i)
    

def handle_camera_stream() -> None:
    all_cams = list_hot_cameras_on_my_device()
    session_state.model_mounted = True

def on_upload(model, linear_points: list) -> None:
    if session_state.get("uploaded_file") is not None: # if a file is uploaded
        video_file = session_state.uploaded_file
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