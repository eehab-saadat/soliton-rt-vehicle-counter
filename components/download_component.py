import streamlit as st
from os import listdir
from utils.stats import render_statistics
from pandas import read_csv
from os.path import exists
from os import makedirs

@st.dialog(title="Download File", width="large")
def file_downloader(output="storage") -> None:
    if not exists(output):
        makedirs(output)
    filename = st.selectbox(label="Select file to download.", options=listdir(output))
    if filename == "" or filename is None:
        st.write("No file selected or no file present.")
        return
    with open(output + "/" +filename, "r") as file:
        st.download_button("Download",
                    data=file,
                    file_name=filename,
                    mime="text/csv")
    st.session_state.data_for_visualization = read_csv( output + "/" + filename)
    render_statistics()