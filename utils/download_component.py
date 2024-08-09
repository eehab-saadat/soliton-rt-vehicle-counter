import streamlit as st
from os import listdir
from stats import render_statistics

def frag():
    render_statistics()

@st.dialog(title="Download File", width="large")
def file_downloader() -> None:
    filename = st.selectbox("Select file to download.", listdir("storage"))

    with open("storage/"+filename, "r") as file:
        st.download_button("Download", 
                    data=file,
                    file_name=filename,
                    mime="text/csv")
    
    frag()

    
st.title("Download File")
st.button("Click Me", on_click=file_downloader)


myvar = "Hello World"
myvar