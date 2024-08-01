from classes.model import MODEL
from ultralytics import YOLO
model = MODEL()
model.mount(YOLO(model='weights/final.pt'))
region_points = [(500, 450), (550, 450), (550, 900), (500, 900)]
linear_points = [(500, 450), (500, 1300)]
model.count("samples/sample.mp4", 1, linear_points)
# mydict = {"bike":{"IN":1, "OUT":2}, "car":{"IN":5, "OUT":5}}
# model.execute(skip=10)