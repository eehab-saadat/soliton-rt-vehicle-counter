from copy import deepcopy
from csv import writer
from ultralytics import YOLO, solutions
from ultralytics.solutions import ObjectCounter
from cv2 import imshow, waitKey, destroyAllWindows, VideoCapture
from cv2 import CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_POS_FRAMES
import streamlit as st

class MODEL:
    __model = None
    
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        if isinstance(self.__model, YOLO):
            return "<class 'MODEL':YOLO>"
        else:
            return "<class 'MODEL'>"

    def mount(self, model: any) -> None:
        self.__model = model

    def unmount(self) -> None:
        self.__model = None

    def execute(self, source: str = "0", skip: int = 1) -> None:
        if isinstance(self.__model, YOLO):
            try:
                source = source if source != "0" else 0
                for result in self.__model.predict(source=source, task="detect", vid_stride=skip, stream=True, stream_buffer=True):
                    frame = result.plot()
                    imshow('Video', frame)
                    if waitKey(1) == ord('q'):
                        break
            except Exception as e:
                print(f"Error occurred: {e}")
            destroyAllWindows()
        elif self.__model is None:
            print("No model detected. Mount a model first using `MODEL.mount(your_model)`")
        else:
            print("Operation unsupported for the mounted model.")

    def __dump(self, counts: dict) -> None:
        classes = self.__model.names
        with open("counts.csv", "w", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerow(["class", "counts"])
            for cls in list(classes.values()):
                if cls in list(counts.keys()):
                    csv_writer.writerow([cls, counts[cls]["IN"]])
                else:
                    csv_writer.writerow([cls, 0])

    def __clean_count(self, counts: dict) -> None:
        print(f"\nRAW = {counts}")
        print("Object Counts:")
        for cls, val in counts.items():
            if isinstance(val, dict):
                keys = list(val.keys())
                if "IN" in keys and "OUT" in keys:
                    for direction in keys:
                        print(f"{cls.capitalize()} ({direction}) = {val[direction]}")

    def count(self, source: str = "0", skip: int = 1, region_points: list = [], resolution: tuple = (1280, 720), show_vid: bool = False) -> None:
        if isinstance(self.__model, YOLO):
            try:
                frame_width, frame_height = resolution
                frame_count = 0
                source = source if source != "0" else 0
                capture = VideoCapture(source)
                capture.set(CAP_PROP_FRAME_WIDTH, frame_width)
                capture.set(CAP_PROP_FRAME_HEIGHT, frame_height)
                
                object_counter = ObjectCounter(
                    view_img=show_vid,
                    reg_pts=region_points,
                    classes_names=self.__model.names,
                    draw_tracks=True,
                    line_thickness=2
                )

                new_classwise_count = {}
                old_classwise_count = {}

                while capture.isOpened():
                    success, im0 = capture.read()
                    if not success:
                        break
                    tracks = self.__model.track(im0, persist=True, show=False, verbose=False)
                    im0 = object_counter.start_counting(im0, tracks)

                    # updt the frame in session state
                    st.session_state.frame_bucket.image(im0, channels="BGR")

                    new_classwise_count = object_counter.class_wise_count

                    if new_classwise_count != old_classwise_count:
                        self.__clean_count(new_classwise_count)
                        self.__dump(new_classwise_count)
                        old_classwise_count = deepcopy(new_classwise_count)

                    frame_count += skip
                    capture.set(CAP_PROP_POS_FRAMES, frame_count)
                    if waitKey(1) == ord('q'):
                        break

                capture.release()
                destroyAllWindows()
                
            except Exception as e:
                print(f"Error occurred: {e}")
        elif self.__model is None:
            print("No model detected. Mount a model first using `MODEL.mount(your_model)`")
        else:
            print("Operation unsupported for the mounted model.")