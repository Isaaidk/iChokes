FROM python:3.12-slim

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY roboflow-object-detection-app/backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY roboflow-object-detection-app/backend ./backend
COPY roboflow-object-detection-app/frontend ./frontend

RUN mkdir -p /usr/src/app/backend/app/static/uploads /usr/src/app/backend/app/static/outputs

ENV PYTHONPATH=/usr/src/app/backend

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
