# Backend Docker Deployment

## Construcción

Desde la carpeta `roboflow-object-detection-app`:

```bash
docker compose build
```

## Ejecución

```bash
docker compose up -d
```

## Acceso

- Frontend: http://localhost
- Backend API: http://localhost:8000

## Archivos importantes

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`
- `frontend/default.conf`
- `backend/.env`

## Variables de entorno

Asegúrate de que `backend/.env` contiene:

```dotenv
ROBOFLOW_API_KEY=tu_api_key
MODEL_ID=tu_modelo
API_URL=https://serverless.roboflow.com
```

> No subas el `.env` a repositorios públicos con tus claves.
