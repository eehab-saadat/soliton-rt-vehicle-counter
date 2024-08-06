from utils.onlycams import list_hot_cameras_on_my_device
from streamlit import session_state, rerun
from tempfile import NamedTemporaryFile
from utils.dialogBox import showDialogBox
from classes.model import MODEL
from classes.inference import INSTANCE


def runInstance(model: MODEL, args: tuple):
    instance = INSTANCE()
    instance.add(model.count, args=args)
def handle_camera_stream(model: MODEL, toSkip: int, linear_points: list) -> None:
    all_cams = list_hot_cameras_on_my_device()
    session_state.model_mounted = True
    session_state.menu_options = [session_state.selected]
    runInstance(model, (all_cams[session_state.selected_cam], toSkip, linear_points))

    # model.count(source=all_cams[session_state.selected_cam], skip=2, region_points=linear_points)

def on_upload(model: MODEL, linear_points: list) -> None:
    if session_state.get("uploaded_file") is not None: # if a file is uploaded
        video_file = session_state.uploaded_file
        session_state.menu_options = [session_state.selected]
        # model.count(src=video_file.upload_url)

        # create a temporary copy of the uploaded file in storage folder
        with NamedTemporaryFile(delete=False, suffix=video_file.name.split(".")[-1]) as temp:
            temp.write(video_file.read())
            model.count(temp.name, 1, linear_points)
        
    else:
        # TODO: show error message popup
        showDialogBox(heading="Upload Error", 
                      message="File not uploaded properly. file not present, incompatible format or file size > 200mb.")
        
def handle_ip_stream(model: MODEL, source: str, toSkip: int, linear_points: list) -> None:
    model.count(source=source, skip=1, region_points=linear_points)
    #TODO: add error handling for invalid IP addresses
    pass