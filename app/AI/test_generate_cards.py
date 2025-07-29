import os
from pathlib import Path
from PIL import Image
import io
import sys

# YOLO 기반 카드 생성 모듈 가져오기
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.services.image_processing import generate_cards_from_bytes

# 테스트 이미지 경로
TEST_IMAGE_DIR = Path(__file__).parent / "test_photos" 

# 결과 저장 폴더
OUTPUT_DIR = Path(__file__).parent / "test_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    # test_photos 폴더 내의 이미지 파일 가져오기
    image_files = list(TEST_IMAGE_DIR.glob("*.[pjPJ][pnPN]*[gG]"))
    
    if not image_files:
        print("❌ test_photos 폴더에 테스트할 이미지가 없습니다.")
        return

    for img_path in image_files:
        print(f"🖼️ 처리 중: {img_path.name}")

        with open(img_path, "rb") as f:
            img_bytes = f.read()

        try:
            # 출력 파일명은 원래 이미지 이름과 동일하게
            output_filename = img_path.stem + "_card.jpg"
            output_path = OUTPUT_DIR / output_filename

            card_img = generate_cards_from_bytes(img_bytes, output_path=str(output_path))

            print(f"✅ 완료: {output_path.name}")

        except Exception as e:
            print(f"❌ 에러 ({img_path.name}): {e}")

if __name__ == "__main__":
    main()
