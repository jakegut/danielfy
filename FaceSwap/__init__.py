import typing as t
import cv2
import io
import urllib.request as r
import mimetypes
import numpy as np
import random

from .face_detection import select_face
from .face_swap import face_swap as fs


class RandomFaceSwap():

    loaded_imgs = []

    def __init__(self, imgs: t.List[str]):
        for img in imgs:
            self.loaded_imgs.append(cv2.imread(img))
        print(len(self.loaded_imgs), "imgs loaded")

    def is_url_image(self, url):
        mimetype, encoding = mimetypes.guess_type(url)
        return (mimetype and mimetype.startswith('image'))

    def load_remote_img(self, remote_url):
        # if not self.is_url_image(remote_url):
        #     return "Could not determine if URL is image"
        req = r.urlopen(remote_url)
        if req is None:
            return "Could not open URL"
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        if arr is None:
            return "Well, shit sorry ya'll"
        return cv2.imdecode(arr, -1)

    def face_swap(self, src_img_url):
        src_img = self.load_remote_img(src_img_url)
        if src_img is None:
            return "Could not load image"
        elif isinstance(src_img, str):
            return src_img
        dst_img = random.choice(self.loaded_imgs)

        # Select src face
        src_points, src_shape, src_face = select_face(src_img)
        # Select dst face
        dst_points, dst_shape, dst_face = select_face(dst_img)

        if src_points is None or dst_points is None:
            return "Did not detect face"

        args = {
            'correct_color': True,
            'warp_2d': True
        }

        output = fs(src_face, dst_face, src_points, dst_points, dst_shape,
                    dst_img, args)

        is_success, buffer = cv2.imencode(".jpg", output)
        return io.BytesIO(buffer)
