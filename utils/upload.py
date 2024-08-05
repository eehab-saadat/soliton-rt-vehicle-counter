from streamlit import session_state, dialog
from tempfile import NamedTemporaryFile
from utils.dialogBox import showDialogBox

def on_upload() -> None:
    if session_state.get("uploaded_file") is not None: # if a file is uploaded
        video_file = session_state.uploaded_file
        session_state.menu_options =[session_state.selected]
        # model.count(src=video_file.upload_url)
        # create a temporary copy of the uploaded file in storage folder
        with NamedTemporaryFile(delete=False, suffix=video_file.name.split(".")[-1]) as temp:
            temp.write(video_file.read())
            # model.count(temp.name, 1, linear_points)
        
    else:
        # TODO: show error message popup
        showDialogBox(heading="Upload Error", 
                      message="File not uploaded properly. file not present, incompatible format or file size > 200mb.")