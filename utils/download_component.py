import streamlit as st
from os import listdir

@st.dialog(title="Download File")
def file_downloader() -> None:
    filename = st.selectbox("Select file to download.", listdir("storage"))

    with open("storage/"+filename, "r") as file:
        st.download_button("Download", 
                    data=file,
                    file_name=filename,
                    mime="text/csv")
        
        
st.button("Click Me", on_click=file_downloader)