# Task Manager API

API REST para gestionar tareas y usuarios, desarrollada con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- psycopg
- Pydantic
- pydantic-settings
- pwdlib
- Argon2
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
- Validación de emails
- Protección frente a emails duplicados
- Hash seguro de contraseñas con Argon2
- Acceso a PostgreSQL mediante SQLAlchemy
- Configuración centralizada con `pydantic-settings`
- Organización de endpoints mediante routers
- Base de datos PostgreSQL separada para tests
- Tests automáticos del CRUD y registro de usuarios
- Análisis estático y linting con Ruff
- Integración continua con GitHub Actions

## Estructura del proyecto

```text id="th89qc"
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── tasks.py
│       └── users.py
├── tests/
│   └── test_main.py
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash id="cb7wwp"
git clone https://github.com/sergiof11/task-manager-api.git
cd task-manager-api
```

### 2. Crear un entorno virtual

```bash id="0rwpgm"
python -m venv venv
```

### 3. Activar el entorno virtual

#### Windows PowerShell

```powershell id="hl5xdb"
.\venv\Scripts\Activate
```

#### Linux / macOS

```bash id="ssn33q"
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash id="ycb8ll"
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` a partir de `.env.example`.

Ejemplo:

```env id="un6z42"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=gestor_tareas
DB_USER=postgres
DB_PASSWORD=your_password_here
```

También es necesario tener PostgreSQL instalado y crear una base de datos llamada:

```text id="ukq09n"
gestor_tareas
```

Para los tests se utiliza una base de datos PostgreSQL separada:

```text id="qrgfse"
gestor_tareas_test
```

La configuración de la aplicación se centraliza en `app/config.py` mediante `pydantic-settings`.

## Ejecutar la API

Con el entorno virtual activado:

```bash id="1paoup"
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

```text id="17r5bv"
http://127.0.0.1:8000
```

La documentación interactiva de FastAPI estará disponible en:

```text id="0xwb0v"
http://127.0.0.1:8000/docs
```

## Endpoints

### Tasks

#### Obtener todas las tareas

```http id="aeihmn"
GET /tasks
```

#### Obtener una tarea

```http id="yt6of7"
GET /tasks/{task_id}
```

#### Crear una tarea

```http id="vl59js"
POST /tasks
```

Ejemplo:

```json id="0mkuvn"
{
  "title": "Estudiar FastAPI"
}
```

El campo `completed` es opcional al crear una tarea y por defecto es `false`.

#### Actualizar una tarea

```http id="yn8gg9"
PUT /tasks/{task_id}
```

Ejemplo:

```json id="1j5578"
{
  "title": "Estudiar FastAPI y PostgreSQL",
  "completed": true
}
```

#### Eliminar una tarea

```http id="ivlz9b"
DELETE /tasks/{task_id}
```

### Users

#### Registrar un usuario

```http id="n7gm94"
POST /users/register
```

Ejemplo:

```json id="swhwm7"
{
  "email": "user@example.com",
  "password": "Password123"
}
```

Las contraseñas no se almacenan en texto plano. Se transforman mediante Argon2 antes de guardarse en PostgreSQL.

El email debe tener un formato válido y no puede estar registrado previamente.

## Tests

El proyecto utiliza `pytest` y una base de datos PostgreSQL separada para evitar que los tests modifiquen los datos de desarrollo.

Ejecutar todos los tests:

```bash id="pj3vqe"
python -m pytest
```

Actualmente el proyecto cuenta con 12 tests que comprueban:

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

## Calidad de código

El proyecto utiliza Ruff para analizar el código y detectar problemas de estilo, imports y posibles errores.

Ejecutar Ruff:

```bash id="zg7ehv"
ruff check .
```

Antes de realizar commits importantes se recomienda ejecutar:

```bash id="0b6i7y"
ruff check .
python -m pytest
```

## Integración continua

El proyecto utiliza GitHub Actions para ejecutar automáticamente las comprobaciones de calidad y los tests después de cada `push` y en los pull requests.

El workflow de CI:

- crea un entorno Ubuntu temporal
- levanta un servicio PostgreSQL para tests
- instala Python y las dependencias del proyecto
- ejecuta Ruff
- ejecuta los tests con pytest

La configuración se encuentra en:

```text id="nt226y"
.github/workflows/ci.yml
```

## Próximas mejoras

- Migraciones de base de datos con Alembic
- Login de usuarios
- Autenticación con JWT
- Protección de endpoints
- Relación entre usuarios y tareas
- Autorización para aislar las tareas de cada usuario
- Paginación y filtros en tareas
- Healthcheck y manejo de errores
- Cobertura de tests con `pytest-cov`
- Docker y Docker Compose
- CI completo con PostgreSQL de test y migraciones
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
- hashing de contraseñas con Argon2
- validación de datos
- configuración centralizada con `pydantic-settings`
- organización de rutas mediante routers
- base de datos de test separada
- 12 tests automáticos
- análisis de código con Ruff
- CI básico con GitHub Actions

La siguiente fase estará centrada en introducir migraciones de base de datos con Alembic.