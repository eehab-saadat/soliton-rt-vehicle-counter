import streamlit as st
from os import listdir
from utils.stats import render_statistics
from pandas import read_csv

@st.dialog(title="Download File", width="large")
def file_downloader() -> None:
    filename = st.selectbox(label="Select file to download.", options=listdir("storage"))

    with open("storage/"+filename, "r") as file:
        st.download_button("Download",
                    data=file,
                    file_name=filename,
                    mime="text/csv")
    st.session_state.data_for_visualization = read_csv( "storage/" + filename)
    render_statistics()