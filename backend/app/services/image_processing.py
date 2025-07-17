import io
import os
from typing import Tuple,List

import cv2
from PIL import Image
from ultralytics import YOLO

# ──────────────────────────────────────────────
# 1. YOLO 모델 로드 (전역·싱글톤)
# ──────────────────────────────────────────────
MODEL_NAME = os.getenv("YOLO_WEIGHTS","yolov8n.pt") #GPU 미사용시 yolo8n.pt(나노), yolov8s.pt(스물)로 시작 
model = YOLO(MODEL_NAME)

# ──────────────────────────────────────────────
# 2. 타입 힌트
# ──────────────────────────────────────────────
BBox = Tuple[int, int, int, int]        # (x1, y1, x2, y2)

# ──────────────────────────────────────────────
# 3. 사람 탐지 함수
# ──────────────────────────────────────────────
def detect_human(img_bytes:bytes, conf_threshold: float=0.4) ->List[BBox]:
    results = model.predict(
        img_bytes,
        imgsz=640,
        conf=conf_threshold,
        classes=[0],
        verbose=False
    )
    bboxes: List[BBox] = []
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0: #확실히 사람
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                bboxes.append(int(x1), int(y1), int(x2), int(y2))
    return bboxes

# ──────────────────────────────────────────────
# 4. bbox → 카드용 이미지로 크롭 & 정형화
# ──────────────────────────────────────────────

def crop_and_normalize(
    img: Image.Image,
    bbox: BBox,
    card_size: Tuple[int, int] = (400, 560),
    bg_color=(255, 255, 255),
) -> Image.Image:
    """
    1) bbox 기준으로 사람 영역 crop
    2) 카드 비율(기본 4:5) 유지하며 중앙 배치·패딩
    3) 최종 card_size 로 리사이즈
    """
    x1, y1, x2, y2 = bbox
    person_img = img.crop((x1, y1, x2, y2))

   # 비율 유지하며 썸네일
    target_w, target_h = card_size
    person_img.thumbnail(card_size, Image.LANCZOS)

    # 새 캔버스에 중앙 정렬
    canvas = Image.new("RGB", card_size, bg_color)
    paste_x = (target_w - person_img.width) // 2
    paste_y = (target_h - person_img.height) // 2
    canvas.paste(person_img, (paste_x, paste_y))

    return canvas

# ──────────────────────────────────────────────
# 5. 업로드된 원본을 → 카드 이미지 리스트로 변환
# ──────────────────────────────────────────────
def generate_cards_from_bytes(
    img_bytes: bytes,
    max_cards: int = 6,
    card_size: Tuple[int, int] = (400, 500),
) -> List[Image.Image]:
    """
    원본 바이트 입력 → PIL 카드 이미지 리스트 반환
    - 사람 bbox 여러 개면 여러 장 생성
    - max_cards 개수 제한
    """
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    bboxes = detect_human(img_bytes)

    cards: List[Image.Image] = []
    for bbox in bboxes[:max_cards]:
        card_img = crop_and_normalize(img, bbox, card_size=card_size)
        cards.append(card_img)
    return cards

