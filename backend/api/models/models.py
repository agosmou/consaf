import yolov5


class Users:
    def __init__(self, data):
        self.data = data


class YOLOv5Model:
    def __init__(self):
        self.model = yolov5.load("keremberke/yolov5n-construction-safety")
        self.model.conf = 0.25
        self.model.iou = 0.45
        self.model.agnostic = False
        self.model.multi_label = False
        self.model.max_det = 1000
        # relevant labels {3: 'Gloves', 4: 'Hardhat', 5: 'Mask', 6: 'NO-Hardhat', 7: 'NO-Mask', 8: 'NO-Safety Vest', 10: 'Safety Net', 11: 'Safety Shoes', 12: 'Safety Vest'}
