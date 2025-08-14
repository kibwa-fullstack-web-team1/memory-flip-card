# 멀티스테이지 빌드를 위한 빌드 스테이지
FROM python:3.11-slim AS builder

# 빌드 의존성 설치
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# 가상환경 생성
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 프로덕션 스테이지
FROM python:3.11-slim

# YOLO 설정 저장 디렉토리 환경 변수 
ENV YOLO_CONFIG_DIR=/app/yolo-config
# 가상환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 런타임 의존성만 설치 (빌드 도구 제외)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libjpeg62-turbo \
    libpng16-16 \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*

WORKDIR /app

# 애플리케이션 코드 복사
COPY . .

# 최종 정리 (혹시 모를 임시 파일들 제거)
RUN rm -rf /tmp/* /var/tmp/* 2>/dev/null || true

EXPOSE 8020

CMD ["python", "main.py"]