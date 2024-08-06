from utils.onlycams import list_hot_cameras_on_my_device
from streamlit import session_state
from main import count
from threading import Thread

def handle_camera_stream() -> None:
    all_cams = list_hot_cameras_on_my_device()
    session_state.model_mounted = True
    session_state.menu_options = [session_state.selected]
    count()