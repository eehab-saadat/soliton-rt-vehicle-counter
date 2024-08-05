from streamlit import session_state
from tempfile import NamedTemporaryFile

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
        print("file not uploaed")