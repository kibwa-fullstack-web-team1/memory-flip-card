from typing import List
import numpy as np
from PIL import Image
import torch
from io import BytesIO
from ultralytics import YOLO

# YOLO 모델 로드 (사람 감지를 위한 COCO pre-trained)
model = YOLO("yolov8n.pt")  # 작은 모델로 빠르게 처리

def generate_cards_from_bytes(image_bytes: bytes) -> List[Image.Image]:
    """
    YOLO를 사용하여 이미지 바이트에서 얼굴을 감지하고 카드 이미지 리스트를 생성합니다.
    """
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    results = model.predict(image, classes=[0], conf=0.4)  # 클래스 0은 'person'

    if not results or not results[0].boxes:
        return []

    boxes = results[0].boxes.xyxy.cpu().numpy()
    
    # 모든 사람을 포함하는 단일 카드 생성
    if len(boxes) > 0:
        min_x = int(min(box[0] for box in boxes))
        min_y = int(min(box[1] for box in boxes))
        max_x = int(max(box[2] for box in boxes))
        max_y = int(max(box[3] for box in boxes))
        
        cropped = image.crop((min_x, min_y, max_x, max_y))
        card_img = cropped.resize((512, 512), Image.LANCZOS)
        return [card_img]
        
    return []
