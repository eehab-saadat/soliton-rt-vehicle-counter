import streamlit as st
from tempfile import NamedTemporaryFile

def on_upload() -> None:
    if st.session_state.get("input_option_bucket") is not None: # if a file is uploaded
        video_file = st.session_state.input_option_bucket.uploaded_file
        # model.count(src=video_file.upload_url)
        # create a temporary copy of the uploaded file in storage folder
        with NamedTemporaryFile(delete=False, suffix=video_file.name.split(".")[-1]) as temp:
            temp.write(video_file.read())
            # model.count(temp.name, 1, linear_points)
        
    else:
        # TODO: show error message popup
        print("file not uploaed")