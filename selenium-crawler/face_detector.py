from detection.core.mtcnn import MTCNN

class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()
        
    def detect(self, img, **kwargs):
        return self.detector.detect(img=img, **kwargs)