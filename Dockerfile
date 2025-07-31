FROM python:3.12-slim

# YOLO 설정 저장 디렉토리 환경 변수 
ENV YOLO_CONFIG_DIR=/app/yolo-config

# opencv 라이브러리 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#. /app
COPY . . 

EXPOSE 8020

CMD ["python", "main.py"]
