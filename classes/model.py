from ultralytics import YOLO
from cv2 import imshow, waitKey, destroyAllWindows

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