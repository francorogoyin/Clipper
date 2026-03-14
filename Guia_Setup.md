# Guía de setup manual

Pasos que tenés que hacer vos para dejar
todo funcionando.

---

## 1. Instalar dependencias del sistema

### Docker Desktop

Necesario para correr PostgreSQL y Redis
en desarrollo.

1. Descargar de https://docker.com/products/docker-desktop
2. Instalar y reiniciar.
3. Verificar: `docker --version`.

### Node.js (v20+)

Para el frontend React.

1. Descargar de https://nodejs.org
2. Instalar la versión LTS.
3. Verificar: `node --version`.

### Pandoc

Necesario para exportar a DOC y ODT
(pypandoc lo usa internamente).

1. Descargar de https://pandoc.org/installing.html
2. Instalar y verificar: `pandoc --version`.

---

## 2. Levantar base de datos

Desde la raíz del proyecto:

```bash
docker compose up -d
```

Esto levanta PostgreSQL (puerto 5432) y
Redis (puerto 6379).

---

## 3. Configurar variables de entorno

1. Copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

2. Generar claves:

```bash
# Secret key para JWT.
openssl rand -hex 32

# Fernet key para encriptar tokens.
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

3. Pegar los valores generados en `.env`.

---

## 4. Crear integración OAuth de Google

1. Ir a https://console.cloud.google.com
2. Crear un proyecto nuevo (o usar existente).
3. Ir a "APIs & Services" → "Credentials".
4. Click "Create Credentials" → "OAuth client ID".
5. Tipo: "Web application".
6. Authorized redirect URIs: agregar
   `http://localhost:8000/api/auth/google/callback`
7. Copiar Client ID y Client Secret al `.env`:
   - `GOOGLE_CLIENT_ID=...`
   - `GOOGLE_CLIENT_SECRET=...`
8. En "OAuth consent screen", configurar:
   - App name: Highlighter
   - Scopes: email, profile, openid

---

## 5. Crear integración OAuth de Notion

Para OAuth público (no internal integration):

1. Ir a https://www.notion.so/my-integrations
2. Click "New integration".
3. Nombre: Highlighter.
4. Tipo: **Public** (no internal).
5. Redirect URI:
   `http://localhost:8000/api/auth/notion/callback`
6. Copiar OAuth client ID y secret al `.env`:
   - `NOTION_CLIENT_ID=...`
   - `NOTION_CLIENT_SECRET=...`
7. Capabilities: leer contenido, insertar
   contenido, leer info del usuario.

**Importante**: tu integración interna vieja
(secret_...) NO sirve para OAuth público.
Hay que crear una nueva integración pública.

---

## 6. Configurar S3 / Cloudflare R2

Para almacenar archivos subidos y exportados.

### Opción A: Cloudflare R2 (recomendado)

1. Ir a https://dash.cloudflare.com
2. R2 → Create bucket → nombre: "highlighter".
3. R2 → Manage R2 API Tokens → Create API token.
4. Copiar al `.env`:
   - `S3_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com`
   - `S3_ACCESS_KEY=...`
   - `S3_SECRET_KEY=...`
   - `S3_BUCKET_NAME=highlighter`

### Opción B: AWS S3

1. Crear bucket en AWS S3.
2. Crear IAM user con permisos de S3.
3. Copiar credenciales al `.env`.

---

## 7. Instalar dependencias del backend

```bash
cd Backend
pip install -r Requirements.txt
```

---

## 8. Instalar dependencias del frontend

```bash
cd Frontend
npm install
```

---

## 9. Levantar en desarrollo

Terminal 1 — Backend:

```bash
cd Backend
uvicorn App.Principal:App --reload --port 8000
```

Terminal 2 — Frontend:

```bash
cd Frontend
npm run dev
```

La app queda en http://localhost:5173

---

## 10. Deploy en Railway

1. Crear cuenta en https://railway.app
2. Crear nuevo proyecto.
3. Agregar servicios:
   - **Web**: apuntar al repo, configurar
     start command:
     `cd Backend && uvicorn App.Principal:App --host 0.0.0.0 --port $PORT`
   - **PostgreSQL**: agregar servicio de DB.
   - **Redis**: agregar servicio de Redis.
4. Agregar todas las variables de `.env`
   como variables de entorno en Railway.
5. Actualizar las URLs de redirect en
   Google y Notion con el dominio de Railway.
6. Actualizar `FRONTEND_URL` con la URL
   del frontend.

### Dominio personalizado

1. Comprar dominio (Namecheap, Google Domains,
   Cloudflare, etc.).
2. En Railway → Settings → Custom Domain.
3. Configurar DNS (CNAME) según instrucciones
   de Railway.
4. Actualizar redirect URIs en Google y Notion.

---

## Checklist final

- [ ] Docker Desktop instalado y corriendo.
- [ ] PostgreSQL y Redis levantados con docker compose.
- [ ] `.env` completo con todas las variables.
- [ ] OAuth Google configurado y funcionando.
- [ ] OAuth Notion (público) configurado.
- [ ] S3/R2 bucket creado con credenciales.
- [ ] Backend corriendo en puerto 8000.
- [ ] Frontend corriendo en puerto 5173.
- [ ] Login con Google funciona.
- [ ] Login con Notion funciona.
- [ ] Subir un TXT de Kindle y ver highlights.
- [ ] Exportar a PDF y verificar el archivo.
- [ ] Pandoc instalado (para DOC/ODT).
