# Deploy en Railway

Este proyecto puede desplegarse en Railway como un solo servicio Docker.

## Archivos claves

- `Dockerfile` (raíz)
- `backend/Dockerfile` (local o Docker Compose)
- `backend/.env` (variables secretas)
- `frontend/app.js` (usa rutas relativas a la misma app)

## Qué hace este Dockerfile

- Instala Python y dependencias
- Copia `backend` y `frontend`
- Sirve la API FastAPI y el frontend estático desde el mismo contenedor

## Pasos para deploy en Railway

1. Sube el repositorio a GitHub.
2. Crea una cuenta en https://railway.app.
3. Crea un nuevo proyecto y selecciona "Deploy from GitHub".
4. Conecta tu repositorio.
5. Railway detectará el `Dockerfile` en la raíz del proyecto y lo usará para construir.
6. Configura las variables en Railway:
   - `ROBOFLOW_API_KEY`
   - `MODEL_ID`
   - `API_URL=https://serverless.roboflow.com`
   - `PORT` no es necesario definir, Railway lo asigna automáticamente y el Dockerfile lo usa con `${PORT:-8000}`.
7. Despliega.

## URL del frontend

La app se servirá desde la URL que Railway te entregue para el servicio.

## Variables de entorno

En Railway debes agregar:

```dotenv
ROBOFLOW_API_KEY=tu_api_key
MODEL_ID=tu_modelo
API_URL=https://serverless.roboflow.com
```

## Notas

- El frontend ya usa rutas relativas, así que no necesitas cambiar `API_URL` si todo está en el mismo servicio.
- Si quieres usar otro hosting para frontend, entonces actualiza `frontend/app.js` con la URL del backend.
