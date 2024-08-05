# from pygrabber.dshow_graph import FilterGraph
# import streamlit as st

# # global graph
# # graph = FilterGraph()

# class FilterGraphSingleton:
#     _instance = None

#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(FilterGraphSingleton, cls).__new__(cls)
#             cls._instance._initialize(*args, **kwargs)
#         return cls._instance

#     def _initialize(self, *args, **kwargs):
#         self.graph = FilterGraph()

#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = cls()
#         return cls._instance

# def list_hot_cameras_on_my_device():
#     graph = FilterGraphSingleton.get_instance().graph
#     cameras = {}
#     devices = graph.get_input_devices()
#     for i, device in enumerate(devices):
#         cameras[device] = i
#     return cameras

from cv2_enumerate_cameras import enumerate_cameras

def list_hot_cameras_on_my_device():
    devices = {}
    index = 0
    for camera in enumerate_cameras():
        if camera.name not in list(devices.keys()):
            devices[camera.name] = index
            index += 1
        else:
            continue
    return devices

if __name__ == "__main__":
    print(list_hot_cameras_on_my_device())