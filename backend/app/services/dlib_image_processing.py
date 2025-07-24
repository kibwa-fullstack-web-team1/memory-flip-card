import cv2
import dlib
import numpy as np
from PIL import Image

def crop_face_with_padding(image_path, output_size=(400, 500)):
    detector = dlib.get_frontal_face_detector()
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("이미지를 불러올 수 없습니다.")
    return _process_face_crop(img, detector, output_size)

def crop_face_from_bytes(image_bytes: bytes, output_size=(400, 500)) -> Image.Image:
    """dlib를 사용하여 이미지 바이트에서 얼굴을 크롭합니다."""
    detector = dlib.get_frontal_face_detector()
    
    # 바이트를 numpy 배열로 변환
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("이미지 데이터를 디코딩할 수 없습니다.")

    # 얼굴 크롭 처리
    processed_img_cv2 = _process_face_crop(img, detector, output_size)
    
    # OpenCV(BGR) 이미지를 PIL(RGB) 이미지로 변환
    processed_img_rgb = cv2.cvtColor(processed_img_cv2, cv2.COLOR_BGR2RGB)
    return Image.fromarray(processed_img_rgb)

def _process_face_crop(img: np.ndarray, detector, output_size: tuple):
    """얼굴을 찾아 크롭하는 핵심 로직"""
    height, width = img.shape[:2]
    orientation = "landscape" if width > height else "portrait"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        raise ValueError("이미지에서 얼굴을 찾을 수 없습니다.")

    x1_all = min([face.left() for face in faces])
    y1_all = min([face.top() for face in faces])
    x2_all = max([face.right() for face in faces])
    y2_all = max([face.bottom() for face in faces])

    face_group_width = x2_all - x1_all
    face_group_height = y2_all - y1_all

    if orientation == "portrait":
        left_right_ratio = 0.1
        top_ratio = 0.25
        bottom_ratio = 0.6
    else:
        left_right_ratio = 0.25
        top_ratio = 0.2
        bottom_ratio = 0.4

    pad_x = int(face_group_width * left_right_ratio)
    pad_y_top = int(face_group_height * top_ratio)
    pad_y_bottom = int(face_group_height * bottom_ratio)

    crop_x1 = max(x1_all - pad_x, 0)
    crop_x2 = min(x2_all + pad_x, img.shape[1])
    crop_y1 = max(y1_all - pad_y_top, 0)
    crop_y2 = min(y2_all + pad_y_bottom, img.shape[0])

    cropped = img[crop_y1:crop_y2, crop_x1:crop_x2]

    desired_ratio = output_size[0] / output_size[1]
    current_h, current_w = cropped.shape[:2]
    current_ratio = current_w / current_h

    if current_ratio < desired_ratio:
        new_w = int(current_h * desired_ratio)
        pad = (new_w - current_w) // 2
        cropped = cv2.copyMakeBorder(cropped, 0, 0, pad, pad, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    elif current_ratio > desired_ratio:
        new_h = int(current_w / desired_ratio)
        pad = (new_h - current_h) // 2
        cropped = cv2.copyMakeBorder(cropped, pad, pad, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return cv2.resize(cropped, output_size)
