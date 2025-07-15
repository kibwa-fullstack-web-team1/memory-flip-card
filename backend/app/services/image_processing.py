from fastapi import UploadFile
from PIL import Image
import io
from ultralytics import YOLO

class ImageProcessingService:
    def __init__(self):
        self.model = YOLO('yolov8n.pt') # 다른 모델 더 찾아보기

    async def process_image_for_card(self, file:UploadFile):
        # 1. 이미지 파일 읽기
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        np_image = np.array(image) # PIL 이미지를 OpenCV에서 사용 가능한 NumPy 배열로 변환

        # 2. YOLO를 사용하여 사람 객체 탐지
        # results = self.model(np_image) # YOLOv8 사용 예시
        # 여기서 results에서 바운딩 박스, 신뢰도 등을 추출
        # (YOLO 라이브러리 사용법에 따라 결과 파싱 로직 구현)

        # 3. 탐지된 사람 중 핵심 객체 선택 및 중심점 계산
        # (가장 큰 사람, 가장 중앙에 있는 사람 등 기준 설정)
        # if human_detected:
        #    person_bbox = results.xyxy[0][0].tolist() # 예시: 첫 번째 사람 바운딩 박스
        #    x_min, y_min, x_max, y_max, conf, cls = person_bbox
        #    center_x = (x_min + x_max) / 2
        #    center_y = (y_min + y_max) / 2
        # else:
        #    raise ValueError("No human detected in the image.")

        # 4. 비율 보정 및 정규화 (핵심 비즈니스 로직)
        # 카드 목표 비율 (예: 3:4)
        target_aspect_ratio = 3 / 4 # 너비 / 높이

        # 예시적인 정규화 로직 (실제 구현 필요)
        # cropped_image = self._normalize_card_image(np_image, center_x, center_y, target_aspect_ratio)

        # 5. 결과 반환 (BytesIO 형태로 반환하거나, S3에 업로드)
        final_image_pil = Image.fromarray(cropped_image)
        output_io = io.BytesIO()
        final_image_pil.save(output_io, format="PNG") # PNG 또는 JPEG 등 원하는 포맷
        output_io.seek(0)
        return output_io

    # 헬퍼 함수 (이미지 정규화 로직)
    def _normalize_card_image(self, image_np: np.ndarray, center_x: float, center_y: float, target_aspect_ratio: float):
        # 이 함수 내부에 크롭, 리사이즈, 패딩 추가 등 복잡한 로직 구현
        # OpenCV(cv2)를 활용하여 이미지 처리
        # 예: cv2.resize, cv2.getRectSubPix, cv2.copyMakeBorder 등

        # 이 부분은 프로젝트의 구체적인 요구사항에 따라 매우 다르게 구현될 수 있습니다.
        # 목표 크기, 비율, 사람 바운딩 박스를 기준으로 적절한 영역을 잘라내고,
        # 남은 부분을 패딩으로 채우거나 늘려서 목표 비율과 해상도를 맞춥니다.
        return image_np # 임시 반환