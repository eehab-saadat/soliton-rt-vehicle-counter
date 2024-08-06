from csv import writer
from copy import deepcopy
from threading import Thread
from ultralytics import YOLO
from cv2.typing import MatLike
from ultralytics.solutions import ObjectCounter
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES, imshow, waitKey, destroyAllWindows

class MODEL:
    def __init__(self, model: YOLO, source: VideoCapture = None) -> None:
        self.model: YOLO = model
        self.stream: VideoCapture = source
        self.stopped: bool = False
        self.grabbed: bool = False
        self.frame: MatLike = None
        if self.stream is not None:
            (self.grabbed, self.frame) = self.stream.read()
        
    def __str__(self) -> str:
        return "<class 'MODEL'>"

    def start(self, source: VideoCapture = VideoCapture("samples/sample.mp4"), method: str = "count", args: tuple =()) -> None:
        self.stream = source
        (self.grabbed, self.frame) = self.stream.read()
        method_func = getattr(self, method, None)
        if callable(method_func):
            thread : Thread = Thread(target=method_func, args=args)
            thread.start()
            return self
        else:
            return None

    def __dump(self, counts: dict) -> None:
        classes = self.model.names
        with open("counts.csv", "w", newline="") as file:
            csv_writer = writer(file)
            csv_writer.writerow(["class", "counts"])
            for cls in list(classes.values()):
                count_in = counts.get(cls, {}).get("IN", 0)
                csv_writer.writerow([cls, count_in])

    def detect(self, skip: int = 1) -> None:
        pass

    def count(self, skip: int = 3, region_points: list = [(500, 450), (500, 1300)]) -> None:
        frame_count = 0
        object_counter = ObjectCounter(
            reg_pts=region_points,
            classes_names=self.model.names,
            draw_tracks=False,
            line_thickness=0,
            region_thickness=0,
            view_in_counts=False,
            view_out_counts=False
        )
        old_classwise_count = {}
        while not self.stopped:
            (self.grabbed, im0) = self.stream.read()
            if not self.grabbed:
                return
            tracks = self.model.track(im0, persist=True, show=False, verbose=True)
            self.frame = object_counter.start_counting(im0, tracks)

            new_classwise_count = object_counter.class_wise_count

            if new_classwise_count != old_classwise_count:
                self.__dump(new_classwise_count)
                old_classwise_count = deepcopy(new_classwise_count)

            frame_count += skip
            self.stream.set(CAP_PROP_POS_FRAMES, frame_count)

    def read(self) -> MatLike:
        return self.frame
    
    def stop(self) -> None:
        self.stopped = True
        self.stream.release()

if __name__ == "__main__":
    model_instance = MODEL(YOLO("weights/final.pt"), VideoCapture("samples/sample.mp4")).start()
    while True:
        frame = model_instance.read()
        if frame is None:
            break
        imshow("Frame", frame)
        key = waitKey(1) & 0xFF
        if key == ord("q"):
            break
    model_instance.stop()
    destroyAllWindows()