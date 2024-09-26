import streamlit as st
from cv2 import VideoCapture

def get_rtsp_stream(username: str, password: str, ip: str, port: int = 554, channel_no: int = 1, type_no: int = 0) -> VideoCapture:
    # build the url via passed parameters
    url = f"rtsp://{username}:{password}@{ip}:{port}/cam/realmonitor?channel={channel_no}&subtype={type_no}"
    st.write(f"RTSP Stream URL: {url}") # for testing
    # return VideoCapture(url) # return the video capture object to use it in the main app

def display_ip_form() -> None:
    form = st.columns(2)
    username = form[0].text_input("Username") # username input
    password = form[1].text_input("Password") # password input
    ip = form[0].text_input("IP Address") # ip address input
    port = form[1].number_input("Port", value=554) # port input
    channel_no = form[0].number_input("Channel No", value=1) # channel number input
    type_no = form[1].number_input("Type No", value=0) # type number input
    st.button("Get RTSP Stream", on_click=get_rtsp_stream, args=(username, password, ip, port, channel_no, type_no)) # button to get the rtsp stream

display_ip_form()