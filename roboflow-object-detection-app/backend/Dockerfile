FROM python:3.12-slim

WORKDIR /usr/src/app

# =========================
# SYSTEM DEPENDENCIES
# =========================

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# INSTALL PYTHON PACKAGES
# =========================

COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install --no-cache-dir -r ./backend/requirements.txt

# =========================
# COPY PROJECT
# =========================

COPY backend ./backend
COPY frontend ./frontend

# =========================
# CREATE STATIC FOLDERS
# =========================

RUN mkdir -p /usr/src/app/backend/app/static/uploads

RUN mkdir -p /usr/src/app/backend/app/static/outputs

# =========================
# PYTHON PATH
# =========================

ENV PYTHONPATH=/usr/src/app/backend

# =========================
# PORT
# =========================

EXPOSE 8000

# =========================
# START APP
# =========================

CMD ["sh", "-c", "cd backend && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]