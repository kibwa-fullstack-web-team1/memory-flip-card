import os
import numpy as np
from PIL import Image
import torch
from io import BytesIO
from ultralytics import YOLO

# YOLO 모델 로드 (사람 감지를 위한 COCO pre-trained)
model = YOLO("yolov8n.pt")  # 작은 모델로 빠르게 처리

def generate_cards_from_bytes(image_bytes: bytes, output_path: str):
    # 이미지 로드
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_tensor = torch.tensor(np.array(image))

    # 사람 감지 (YOLO는 BGR 아니라 RGB 기반이라 바로 사용 가능)
    results = model.predict(image, classes=[0], conf=0.4)  # 클래스 0은 'person'

    if not results or not results[0].boxes:
        raise ValueError("사람 객체를 찾을 수 없습니다.")

    # 모든 사람 박스 좌표를 수집
    boxes = results[0].boxes.xyxy.cpu().numpy()  # [[x1, y1, x2, y2], ...]
    
    # 전체 인물들을 감싸는 최소 사각형 계산
    min_x = int(min(box[0] for box in boxes))
    min_y = int(min(box[1] for box in boxes))
    max_x = int(max(box[2] for box in boxes))
    max_y = int(max(box[3] for box in boxes))

    # Crop 영역이 이미지 범위를 넘지 않도록 보정
    width, height = image.size
    min_x = max(0, min_x)
    min_y = max(0, min_y)
    max_x = min(width, max_x)
    max_y = min(height, max_y)

    # 인물 중심 crop
    cropped = image.crop((min_x, min_y, max_x, max_y))

    # 카드용으로 리사이징 (예: 512x512)
    card_img = cropped.resize((512, 512), Image.LANCZOS)

    # 결과 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    card_img.save(output_path)
