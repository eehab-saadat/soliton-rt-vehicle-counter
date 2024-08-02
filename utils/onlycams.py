from pygrabber.dshow_graph import FilterGraph
import streamlit as st

global graph
graph = FilterGraph()

def list_hot_cameras_on_my_device():
    cameras = {}
    devices = graph.get_input_devices()
    for i, device in enumerate(devices):
        cameras[device] = i
    return cameras

if __name__ == "__main__":
    print(list_hot_cameras_on_my_device())