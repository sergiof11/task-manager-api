# Task Manager API

API REST para gestionar tareas y usuarios, desarrollada con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg
- Alembic
- Pydantic
- pydantic-settings
- pwdlib
- Argon2
- PyJWT
- pytest
- httpx
- Ruff
- GitHub Actions

## Funcionalidades actuales

- Crear tareas
- Listar tareas
- Obtener una tarea por ID
- Actualizar tareas
- Eliminar tareas
- Validación de datos
- Registro de usuarios
- Login de usuarios
- Generación de access tokens JWT
- Tokens JWT con identificación de usuario y expiración
- Validación de emails
- Protección frente a emails duplicados
- Verificación segura de contraseñas
- Hash seguro de contraseñas con Argon2
- Acceso a PostgreSQL mediante SQLAlchemy
- Migraciones y versionado del esquema con Alembic
- Configuración centralizada con `pydantic-settings`
- Organización de endpoints mediante routers
- Base de datos PostgreSQL separada para tests
- Tests automáticos del CRUD, registro, login y generación de JWT
- Análisis estático y linting con Ruff
- Integración continua con GitHub Actions

## Estructura del proyecto

```text
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   ├── versions/
│   │   └── 902afd450102_initial_schema.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/
│   ├── main.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── auth.py
│       ├── tasks.py
│       └── users.py
├── tests/
│   └── test_main.py
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

Los archivos y carpetas locales como `.env`, `venv/`, `__pycache__/`, `.pytest_cache/` y `.ruff_cache/` están excluidos mediante `.gitignore`.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/sergiof11/task-manager-api.git
cd task-manager-api
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` a partir de `.env.example`.

Ejemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestor_tareas
DB_USER=postgres
DB_PASSWORD=your_password_here

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

También es necesario tener PostgreSQL instalado y crear una base de datos llamada:

```text
gestor_tareas
```

Para los tests se utiliza una base de datos PostgreSQL separada:

```text
gestor_tareas_test
```

La configuración de la aplicación se centraliza en `app/config.py` mediante `pydantic-settings`.

## Migraciones de base de datos

El proyecto utiliza Alembic para gestionar y versionar los cambios del esquema de PostgreSQL.

Aplicar todas las migraciones pendientes:

```bash
alembic upgrade head
```

Comprobar la versión actual de la base de datos:

```bash
alembic current
```

Crear una nueva migración detectando cambios en los modelos SQLAlchemy:

```bash
alembic revision --autogenerate -m "descripcion de la migracion"
```

Deshacer la última migración:

```bash
alembic downgrade -1
```

La aplicación ya no utiliza `Base.metadata.create_all()` para crear o evolucionar las tablas. El esquema de PostgreSQL se gestiona mediante las migraciones de Alembic.

## Ejecutar la API

Antes de iniciar la aplicación, asegúrate de que las migraciones están aplicadas:

```bash
alembic upgrade head
```

Después, con el entorno virtual activado:

```bash
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación interactiva de FastAPI estará disponible en:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### Tasks

#### Obtener todas las tareas

```http
GET /tasks
```

#### Obtener una tarea

```http
GET /tasks/{task_id}
```

#### Crear una tarea

```http
POST /tasks
```

Ejemplo:

```json
{
  "title": "Estudiar FastAPI"
}
```

El campo `completed` es opcional al crear una tarea y por defecto es `false`.

#### Actualizar una tarea

```http
PUT /tasks/{task_id}
```

Ejemplo:

```json
{
  "title": "Estudiar FastAPI y PostgreSQL",
  "completed": true
}
```

#### Eliminar una tarea

```http
DELETE /tasks/{task_id}
```

### Users

#### Registrar un usuario

```http
POST /users/register
```

Ejemplo:

```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

Las contraseñas no se almacenan en texto plano. Se transforman mediante Argon2 antes de guardarse en PostgreSQL.

El email debe tener un formato válido y no puede estar registrado previamente.

### Auth

#### Login de usuario

```http
POST /auth/login
```

Ejemplo:

```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

El endpoint comprueba que el usuario existe y que la contraseña coincide con el hash almacenado.

Si las credenciales son correctas, genera y devuelve un access token JWT:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

El token contiene:

- `sub`: ID del usuario autenticado
- `exp`: fecha y hora de expiración del token

La duración del token se configura mediante:

```text
ACCESS_TOKEN_EXPIRE_MINUTES
```

Si el email no existe o la contraseña es incorrecta, devuelve:

```text
401 Unauthorized
```

La API utiliza el mismo mensaje de error para ambos casos para no revelar si un email concreto está registrado.

La validación de los tokens y la protección de endpoints se implementarán en la siguiente fase.

## Tests

El proyecto utiliza `pytest` y una base de datos PostgreSQL separada para evitar que los tests modifiquen los datos de desarrollo.

Ejecutar todos los tests:

```bash
python -m pytest
```

Actualmente el proyecto cuenta con 15 tests que comprueban:

- listado de tareas
- obtención de una tarea existente por ID
- obtención de una tarea inexistente (`404`)
- creación de tareas
- actualización de tareas
- actualización de una tarea inexistente (`404`)
- eliminación de tareas
- eliminación de una tarea inexistente (`404`)
- validación de títulos formados solo por espacios
- registro de usuarios
- rechazo de emails duplicados
- validación de emails incorrectos
- login con credenciales correctas y generación de JWT válido
- rechazo de login con contraseña incorrecta (`401`)
- rechazo de login con usuario inexistente (`401`)

El test de login correcto también decodifica el JWT generado para comprobar que la firma es válida y que contiene los campos `sub` y `exp`.

## Calidad de código

El proyecto utiliza Ruff para analizar el código y detectar problemas de estilo, imports y posibles errores.

Ejecutar Ruff:

```bash
ruff check .
```

Antes de realizar commits importantes se recomienda ejecutar:

```bash
ruff check .
python -m pytest
```

## Integración continua

El proyecto utiliza GitHub Actions para ejecutar automáticamente las comprobaciones después de cada `push` y en los pull requests.

El workflow de CI:

- crea un entorno Ubuntu temporal
- levanta una instancia PostgreSQL temporal
- instala Python y las dependencias del proyecto
- ejecuta Ruff
- aplica las migraciones con `alembic upgrade head`
- ejecuta los tests con pytest

Esto permite comprobar que una base de datos PostgreSQL vacía puede construirse correctamente utilizando únicamente las migraciones del proyecto.

La configuración se encuentra en:

```text
.github/workflows/ci.yml
```

## Próximas mejoras

- Validación de tokens JWT
- Obtención del usuario autenticado mediante el token
- Protección de endpoints
- Relación entre usuarios y tareas
- Autorización para aislar las tareas de cada usuario
- Paginación y filtros en tareas
- Healthcheck y manejo de errores
- Cobertura de tests con `pytest-cov`
- Refactor de estructura de tests y módulos
- Docker y Docker Compose
- CI completo con cobertura y validaciones adicionales
- Deploy en Azure
- Revisión de secretos y configuración
- README final para portfolio
- Revisión completa y cierre del proyecto

## Estado del proyecto

Proyecto en desarrollo.

Actualmente están implementados:

- CRUD completo de tareas
- PostgreSQL con SQLAlchemy
- separación entre modelos ORM y esquemas Pydantic
- registro de usuarios
- login de usuarios con verificación de credenciales
- hashing de contraseñas con Argon2
- verificación segura de contraseñas
- generación de access tokens JWT
- identificación del usuario mediante el claim `sub`
- expiración de tokens mediante el claim `exp`
- configuración centralizada con `pydantic-settings`
- configuración JWT mediante variables de entorno
- validación de datos
- organización de rutas mediante routers
- migraciones y versionado de base de datos con Alembic
- migración inicial reproducible desde una base de datos vacía
- base de datos de test separada
- 15 tests automáticos
- análisis de código con Ruff
- CI con GitHub Actions, PostgreSQL y migraciones

La siguiente fase estará centrada en validar los access tokens JWT, obtener el usuario autenticado y preparar la protección de endpoints.