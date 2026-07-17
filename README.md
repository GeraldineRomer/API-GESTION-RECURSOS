# API REST con FastAPI, JWT y PostgreSQL

API de gestión con autenticación segura basada en tokens JWT, construida como proyecto de portafolio.

---

## Tecnologías

- **FastAPI** — framework backend moderno y de alto rendimiento
- **PostgreSQL** — base de datos relacional
- **SQLAlchemy** — ORM para manejo de base de datos
- **JWT (JSON Web Tokens)** — autenticación stateless
- **Bcrypt** — hashing seguro de contraseñas
- **Pydantic** — validación de datos de entrada y salida

---

## Funcionalidades

- Registro de usuarios con contraseña encriptada (bcrypt)
- Login con generación de token JWT firmado
- CRUD completo de items protegido por autenticación
- Cada usuario solo puede ver y modificar sus propios datos
- Validación automática de datos en cada endpoint
- Documentación interactiva generada automáticamente en `/docs`

---

## Estructura del proyecto

    fastapi-jwt-api/
    ├── app/
    │   ├── main.py            → punto de entrada de la aplicación
    │   ├── database.py        → conexión a PostgreSQL
    │   ├── models.py          → tablas (SQLAlchemy)
    │   ├── schemas.py         → validación de datos (Pydantic)
    │   ├── auth.py            → lógica de JWT y hashing de contraseñas
    │   ├── dependencies.py    → guardias de seguridad para rutas protegidas
    │   └── routers/
    │       ├── auth_router.py → /auth/register, /auth/login
    │       └── items_router.py → CRUD protegido de items
    ├── requirements.txt
    ├── .example.env
    └── README.md

---

## Endpoints

| Método | Ruta | Descripción | Requiere auth |
|--------|------|-------------|---------------|
| POST | `/auth/register` | Registrar nuevo usuario | No |
| POST | `/auth/login` | Obtener token JWT | No |
| POST | `/items/` | Crear un item | Sí |
| GET | `/items/` | Listar mis items | Sí |
| GET | `/items/{id}` | Obtener un item por ID | Sí |
| DELETE | `/items/{id}` | Eliminar un item | Sí |

---

## Cómo correrlo localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/GeraldineRomer/API-GESTION-RECURSOS.git
cd fastapi-jwt-api
```

### 2. Crear entorno virtual e instalar dependencias

```bash
# Crear entorno virtual
python -m venv .venv

# Activarlo (Windows)
.venv\Scripts\activate

# Activarlo (Mac / Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Crear la base de datos en PostgreSQL

```bash
psql -U postgres
```

```sql
CREATE DATABASE fastapi_jwt_db;
\q
```

### 4. Configurar variables de entorno

Copia el archivo `.example.env` y renómbralo a `.env`:

```bash
cp .env.example .env
```

Luego edita `.env` con tus credenciales reales:

DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/fastapi_jwt_db
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Para generar una `SECRET_KEY` segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Correr el servidor

```bash
uvicorn app.main:app --reload
```

### 6. Abrir la documentación interactiva

http://localhost:8000/docs

---

## Cómo probar la autenticación en /docs

1. Usa `POST /auth/register` para crear un usuario
2. Usa `POST /auth/login` con las mismas credenciales — copia el `access_token` de la respuesta
3. Haz clic en el botón **Authorize** (arriba a la derecha) y pega el token
4. Ya puedes usar los endpoints de `/items/`

---

## Variables de entorno requeridas

| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL |
| `SECRET_KEY` | Clave secreta para firmar los tokens JWT |
| `ALGORITHM` | Algoritmo JWT (usar `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token en minutos |

---

---

## Cómo probar la autenticación en /docs

1. Usa `POST /auth/register` para crear un usuario
2. Usa `POST /auth/login` con las mismas credenciales — copia el `access_token` de la respuesta
3. Haz clic en el botón **Authorize** (arriba a la derecha) y pega el token
4. Ya puedes usar los endpoints de `/items/`

---

## Variables de entorno requeridas

| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL |
| `SECRET_KEY` | Clave secreta para firmar los tokens JWT |
| `ALGORITHM` | Algoritmo JWT (usar `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token en minutos |

---

## Deploy

Esta API está deployada en Railway y disponible en:

🔗 **Demo en vivo: https://api-gestion-recursos-production.up.railway.app/docs

📁 **Repositorio: https://github.com/GeraldineRomer/API-GESTION-RECURSOS

---

## Decisiones técnicas destacadas

- **JWT stateless:** el servidor no guarda sesiones, cada token lleva la información firmada criptográficamente
- **Bcrypt para contraseñas:** nunca se guarda la contraseña en texto plano, solo su hash
- **Separación de schemas y models:** los modelos definen las tablas, los schemas definen qué datos entran y salen por la API — nunca se expone la contraseña en una respuesta
- **Autorización por recurso:** cada usuario solo puede acceder a sus propios items, no a los de otros usuarios aunque estén autenticados
