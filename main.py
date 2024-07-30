from classes.model import MODEL
from ultralytics import YOLO
model = MODEL()
model.mount(YOLO('models/final.pt'))
model.execute(skip=3)