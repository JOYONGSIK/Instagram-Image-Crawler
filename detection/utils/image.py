from pathlib import Path, PosixPath
from typing import Union, List, Tuple

import cv2
import numpy as np
import requests


class Image:
    def __init__(self):
        pass

    @staticmethod
    def load(path_or_bytes: Union[PosixPath, str]) -> np.ndarray:
        if isinstance(path_or_bytes, bytes):
            array = np.fromstring(path_or_bytes, np.uint8)
            return cv2.imdecode(array, cv2.IMREAD_COLOR)
        elif (isinstance(path_or_bytes, str) or
                isinstance(path_or_bytes, PosixPath) and
                Path(path_or_bytes).exists()):
            return Image.load_by_BGR(str(path_or_bytes))
        else:
            raise InvalidFile("Fail to read Image.")

    @staticmethod
    def encode(img, format):
        return cv2.imencode(format, img)
    
    @staticmethod
    def url_load(url):
        image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
        image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        return image

    @staticmethod
    def annotate_green_bboxes(img: np.ndarray, bboxes: List[Union[List, Tuple]]
                        ) -> np.ndarray:
        ret = img.copy()
        for x1, y1, x2, y2 in bboxes:
            cv2.rectangle(ret, (x1, y1), (x2, y2), (0, 255, 0), 3)
        return ret
    
    @staticmethod
    def annotate_red_bboxes(img: np.ndarray, bboxes: List[Union[List, Tuple]]
                            ) -> np.ndarray:
        ret = img.copy()
        for x1, y1, x2, y2 in bboxes:
            cv2.rectangle(ret, (x1, y1), (x2, y2), (0, 0, 255), 3)
        return ret

    @staticmethod
    def save(img: np.ndarray, path: Union[PosixPath, str]) -> None:
        cv2.imwrite(str(path), img)

    @staticmethod
    def is_valid(img):
        if img is None or not hasattr(img, "shape"):
            raise InvalidImage("Invalid Image.")

class InvalidImage(Exception):
    pass


class InvalidFile(Exception):
    pass
