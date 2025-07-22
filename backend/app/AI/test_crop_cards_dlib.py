import os
import sys
import cv2
from pathlib import Path

# dlib 기반 얼굴 크롭 함수 가져오기
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.services.image_processing import crop_face_with_padding

# 테스트 이미지 경로
TEST_IMAGE_DIR = Path(__file__).parent / "test_photos"

# 결과 저장 폴더
OUTPUT_DIR = Path(__file__).parent / "test_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def test_crop_faces_with_dlib():
    image_files = list(TEST_IMAGE_DIR.glob("*.jpg")) + list(TEST_IMAGE_DIR.glob("*.jpeg")) + list(TEST_IMAGE_DIR.glob("*.png"))

    if not image_files:
        print("❗ 테스트 이미지가 없습니다.")
        return

    for img_path in image_files:
        try:
            cropped = crop_face_with_padding(str(img_path))

            output_path = OUTPUT_DIR / f"{img_path.stem}_card{img_path.suffix}"
            cv2.imwrite(str(output_path), cropped)
            print(f"✅ 저장 완료: {output_path.name}")
        except Exception as e:
            print(f"❌ 실패 ({img_path.name}): {e}")

if __name__ == "__main__":
    test_crop_faces_with_dlib()
