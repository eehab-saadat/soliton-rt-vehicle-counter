
from ultralytics import YOLO


model = YOLO("weights/final.pt")
model.export(format="openvino")