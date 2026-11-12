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
- pytest-cov
- httpx
- Ruff
- Docker
- Docker Compose
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
- Validación de access tokens JWT
- Tokens JWT con identificación de usuario y expiración
- Obtención del usuario autenticado mediante JWT
- Endpoint protegido `GET /auth/me`
- Protección mediante JWT de todos los endpoints `/tasks`
- Relación entre usuarios y tareas mediante `user_id`
- Asignación automática del usuario autenticado al crear una tarea
- Foreign key entre `tasks.user_id` y `users.id`
- Índice sobre `tasks.user_id`
- Aislamiento de tareas por usuario
- Listado exclusivo de las tareas del usuario autenticado
- Protección frente al acceso a tareas de otros usuarios
- Protección frente a la modificación de tareas de otros usuarios
- Protección frente a la eliminación de tareas de otros usuarios
- Respuesta `404 Not Found` para tareas inexistentes o pertenecientes a otro usuario
- Paginación de tareas mediante `skip` y `limit`
- Límite máximo de 100 tareas por petición
- Filtro de tareas por estado `completed`
- Validación automática de parámetros de paginación
- Validación de IDs de tareas positivos
- Endpoint público `GET /health`
- Respuestas `401 Unauthorized` para errores de autenticación
- Cabecera `WWW-Authenticate: Bearer` en respuestas `401`
- Mismo mensaje de error para email inexistente y contraseña incorrecta durante el login
- Validación de emails
- Protección frente a emails duplicados
- Respuesta `409 Conflict` al intentar registrar un email existente
- Protección adicional frente a duplicados mediante la restricción `UNIQUE` de PostgreSQL
- Recuperación de la sesión mediante `rollback()` ante conflictos de integridad
- Validación de longitud de contraseñas
- Verificación segura de contraseñas
- Hash seguro de contraseñas con Argon2
- Acceso a PostgreSQL mediante SQLAlchemy
- Consultas parametrizadas mediante SQLAlchemy
- Migraciones y versionado del esquema con Alembic
- Configuración centralizada con `pydantic-settings`
- Organización de endpoints mediante routers
- Base de datos PostgreSQL separada para tests
- Suite de tests organizada por áreas de responsabilidad
- Fixtures compartidas con pytest
- Tests de aislamiento utilizando múltiples usuarios
- Tests de paginación, filtros y casos límite
- Cobertura de código mediante `pytest-cov`
- 100% de cobertura sobre el código de `app/`
- Análisis estático y linting con Ruff
- Contenerización de la API mediante Docker
- Orquestación de FastAPI y PostgreSQL mediante Docker Compose
- Comunicación entre contenedores mediante la red interna de Docker Compose
- Healthcheck de PostgreSQL antes de iniciar la API
- Aplicación automática de migraciones Alembic al iniciar el contenedor de la API
- Persistencia de PostgreSQL mediante un volumen Docker
- Integración continua con GitHub Actions

## Estructura del proyecto

```text
task-manager-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── alembic/
│   ├── versions/
│   │   ├── 902afd450102_initial_schema.py
│   │   └── 5fc071f53c9f_add_user_to_tasks.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/
│   ├── main.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── routers/
│       ├── auth.py
│       ├── tasks.py
│       └── users.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_tasks_authorization.py
│   ├── test_tasks_crud.py
│   ├── test_tasks_filters.py
│   └── test_users.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

Los archivos y carpetas locales como `.env`, `venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/` y los archivos generados por herramientas de cobertura están excluidos mediante `.gitignore` cuando corresponde.

El archivo `.dockerignore` evita copiar al contexto de construcción de Docker archivos innecesarios o sensibles como el entorno virtual, `.env`, cachés, datos de cobertura y metadatos de Git.

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

La configuración de la aplicación se centraliza en `app/config.py` mediante `pydantic-settings`.

### Ejecución local sin Docker

Para ejecutar la aplicación directamente desde el sistema es necesario tener PostgreSQL instalado y crear una base de datos llamada:

```text
gestor_tareas
```

Para los tests se utiliza una base de datos PostgreSQL separada:

```text
gestor_tareas_test
```

Cuando la aplicación se ejecuta localmente, `DB_HOST=localhost` permite conectar FastAPI con la instalación local de PostgreSQL.

### Ejecución con Docker

Cuando el proyecto se ejecuta mediante Docker Compose, PostgreSQL se levanta en un contenedor independiente.

Docker Compose sobrescribe internamente la configuración de conexión para utilizar:

```text
DB_HOST=db
DB_PORT=5432
```

El nombre `db` corresponde al servicio PostgreSQL definido en `docker-compose.yml`.

De esta forma, la API se conecta a PostgreSQL mediante la red interna creada automáticamente por Docker Compose.

## Migraciones de base de datos

El proyecto utiliza Alembic para gestionar y versionar los cambios del esquema de PostgreSQL.

Actualmente existen dos migraciones:

- `902afd450102_initial_schema.py`: crea las tablas iniciales `users` y `tasks`
- `5fc071f53c9f_add_user_to_tasks.py`: añade `user_id` a las tareas y crea la relación con `users`

La relación entre tareas y usuarios utiliza:

- `tasks.user_id`
- foreign key hacia `users.id`
- índice sobre `tasks.user_id`
- restricción `NOT NULL` para garantizar que toda tarea tenga propietario

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

En el entorno Docker, `alembic upgrade head` se ejecuta automáticamente antes de iniciar Uvicorn.

Esto permite crear correctamente el esquema incluso cuando PostgreSQL parte de una base de datos completamente vacía.

## Ejecutar la API localmente

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

## Docker

El proyecto puede ejecutarse mediante Docker Compose, levantando FastAPI y PostgreSQL como servicios independientes.

La arquitectura del entorno es:

```text
Docker Compose
├── api
│   ├── Python 3.11
│   ├── FastAPI
│   ├── Alembic
│   └── Uvicorn
│
└── db
    └── PostgreSQL 16
```

Los dos servicios se comunican mediante una red interna creada automáticamente por Docker Compose.

### Dockerfile

El `Dockerfile` construye la imagen de la API utilizando:

```text
python:3.11-slim
```

Durante la construcción:

1. se establece `/app` como directorio de trabajo
2. se copia `requirements.txt`
3. se instalan las dependencias
4. se copia el código del proyecto
5. se configura Uvicorn como proceso de la aplicación

Construir manualmente la imagen:

```bash
docker build -t task-manager-api .
```

Comprobar las imágenes disponibles:

```bash
docker images
```

### Docker Compose

El archivo `docker-compose.yml` define dos servicios:

- `api`: aplicación FastAPI
- `db`: PostgreSQL 16

PostgreSQL utiliza la imagen oficial:

```text
postgres:16-alpine
```

El servicio `api` se construye utilizando el `Dockerfile` del proyecto.

### Validar la configuración

La configuración de Docker Compose puede comprobarse sin levantar los servicios mediante:

```bash
docker compose config -q
```

Si el comando no devuelve errores, la configuración es válida.

### Levantar el proyecto

Construir la imagen y levantar todos los servicios:

```bash
docker compose up --build
```

Docker Compose:

1. construye la imagen de FastAPI
2. crea la red interna
3. crea el volumen de PostgreSQL
4. inicia PostgreSQL
5. espera a que PostgreSQL esté disponible
6. aplica las migraciones de Alembic
7. inicia Uvicorn

Cuando no se han realizado cambios que requieran reconstruir la imagen, puede utilizarse:

```bash
docker compose up
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Healthcheck de PostgreSQL

El servicio `db` dispone de un healthcheck basado en:

```text
pg_isready
```

La API utiliza `depends_on` con la condición `service_healthy`, por lo que no comienza su proceso de inicio hasta que PostgreSQL está preparado para aceptar conexiones.

Esto evita intentar ejecutar las migraciones o iniciar la aplicación antes de que la base de datos esté disponible.

### Migraciones durante el arranque

El contenedor de la API ejecuta:

```bash
alembic upgrade head
```

antes de iniciar Uvicorn.

El flujo de arranque es:

```text
PostgreSQL
    ↓
healthcheck correcto
    ↓
API
    ↓
alembic upgrade head
    ↓
Uvicorn
    ↓
FastAPI disponible
```

### Persistencia de datos

PostgreSQL utiliza el volumen:

```text
postgres_data
```

Los datos de usuarios y tareas no dependen de la vida del contenedor.

Esto significa que los contenedores pueden detenerse y recrearse sin perder la información almacenada.

La persistencia se ha comprobado recreando los contenedores y verificando posteriormente que usuarios y tareas seguían disponibles.

### Detener los servicios

Detener Docker Compose desde una ejecución en primer plano:

```text
Ctrl+C
```

Eliminar los contenedores y la red del proyecto:

```bash
docker compose down
```

Este comando conserva el volumen de PostgreSQL.

Por tanto, al ejecutar posteriormente:

```bash
docker compose up
```

los datos almacenados siguen disponibles.

### Eliminar también los datos

Para eliminar los contenedores, la red y los volúmenes:

```bash
docker compose down -v
```

Este comando elimina también los datos almacenados por PostgreSQL.

Debe utilizarse únicamente cuando se quiera reiniciar completamente el entorno Docker.

### Recursos de Docker

Las imágenes locales pueden consultarse mediante:

```bash
docker images
```

Los contenedores, incluidos los detenidos, pueden consultarse mediante:

```bash
docker ps -a
```

Una vista más compacta puede obtenerse mediante:

```bash
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
```

Las imágenes colgantes que ya no se utilizan pueden limpiarse mediante:

```bash
docker image prune
```

## Endpoints

### Tasks

Todos los endpoints de tareas están protegidos mediante autenticación JWT.

Es necesario enviar un access token válido mediante la cabecera:

```text
Authorization: Bearer <access_token>
```

Si no se proporciona un token válido, la API devuelve:

```text
401 Unauthorized
```

junto con:

```text
WWW-Authenticate: Bearer
```

Cada tarea almacena internamente el ID del usuario que la creó mediante `user_id`.

El cliente no envía manualmente este valor. La API obtiene el usuario autenticado a partir del JWT y asigna automáticamente:

```text
tasks.user_id = current_user.id
```

Además, todas las operaciones sobre tareas están filtradas por el usuario autenticado.

Esto significa que un usuario únicamente puede listar, consultar, actualizar o eliminar sus propias tareas.

Si intenta acceder a una tarea perteneciente a otro usuario, la API responde:

```text
404 Not Found
```

La API utiliza `404` en lugar de revelar que la tarea existe pero pertenece a otro usuario.

Los IDs de tareas deben ser enteros positivos. Un `task_id` igual o inferior a `0` es rechazado automáticamente con:

```text
422 Unprocessable Entity
```

#### Obtener todas las tareas

```http
GET /tasks
```

Devuelve únicamente las tareas cuyo `user_id` corresponde al usuario autenticado.

El endpoint admite paginación mediante los parámetros:

- `skip`: número de tareas que se omiten. Valor por defecto: `0`
- `limit`: número máximo de tareas devueltas. Valor por defecto: `10`
- `limit` debe estar entre `1` y `100`

Ejemplo:

```http
GET /tasks?skip=0&limit=10
```

También permite filtrar las tareas por su estado:

```http
GET /tasks?completed=true
```

o:

```http
GET /tasks?completed=false
```

Los parámetros pueden combinarse:

```http
GET /tasks?completed=true&skip=0&limit=10
```

La paginación mantiene un orden estable por ID.

FastAPI valida automáticamente los parámetros:

- `skip >= 0`
- `1 <= limit <= 100`
- `completed` debe representar un valor booleano válido

Si los parámetros no cumplen las restricciones definidas, devuelve:

```text
422 Unprocessable Entity
```

#### Obtener una tarea

```http
GET /tasks/{task_id}
```

Solo devuelve la tarea si pertenece al usuario autenticado.

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

El título debe tener entre `1` y `200` caracteres y no puede estar formado únicamente por espacios.

El propietario de la tarea se obtiene automáticamente del usuario autenticado y no debe enviarse en el cuerpo de la petición.

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

Solo se puede actualizar una tarea perteneciente al usuario autenticado.

#### Eliminar una tarea

```http
DELETE /tasks/{task_id}
```

Solo se puede eliminar una tarea perteneciente al usuario autenticado.

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

La contraseña debe tener entre `8` y `128` caracteres.

El email debe tener un formato válido y no puede estar registrado previamente.

Si se intenta registrar un email existente, la API devuelve:

```text
409 Conflict
```

con el mensaje:

```json
{
  "detail": "El email ya está registrado"
}
```

La aplicación realiza una comprobación previa del email y PostgreSQL mantiene además una restricción `UNIQUE` como protección definitiva frente a duplicados.

Si durante la inserción se produce un conflicto de integridad, la sesión de SQLAlchemy realiza `rollback()` y la API responde igualmente con `409 Conflict`.

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

Las contraseñas enviadas al login tienen un límite máximo de `128` caracteres.

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

junto con:

```text
WWW-Authenticate: Bearer
```

La API utiliza el mismo mensaje de error para ambos casos:

```json
{
  "detail": "Email o contraseña incorrectos"
}
```

Esto evita revelar directamente durante el login si un email concreto está registrado.

#### Obtener usuario autenticado

```http
GET /auth/me
```

Este endpoint está protegido y requiere enviar un access token JWT válido mediante la cabecera:

```text
Authorization: Bearer <access_token>
```

La API:

- extrae el token Bearer
- valida la firma del JWT
- comprueba automáticamente su expiración
- obtiene el ID del usuario desde el claim `sub`
- busca el usuario en PostgreSQL
- devuelve únicamente sus datos públicos

Ejemplo de respuesta:

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

Si el token es inválido, ha expirado o hace referencia a un usuario que ya no existe, devuelve:

```text
401 Unauthorized
```

junto con:

```text
WWW-Authenticate: Bearer
```

Un token criptográficamente válido no es suficiente si el usuario indicado por `sub` ya no existe en la base de datos.

### Health

#### Comprobar el estado de la API

```http
GET /health
```

Este endpoint es público y no requiere autenticación.

Ejemplo de respuesta:

```json
{
  "status": "ok"
}
```

Permite comprobar rápidamente que la aplicación está disponible y puede utilizarse en entornos de despliegue o contenedores.

## Tests

El proyecto utiliza `pytest`, `pytest-cov` y una base de datos PostgreSQL separada para evitar que los tests modifiquen los datos de desarrollo.

La suite está organizada por áreas de responsabilidad:

```text
tests/
├── conftest.py
├── test_auth.py
├── test_health.py
├── test_tasks_authorization.py
├── test_tasks_crud.py
├── test_tasks_filters.py
└── test_users.py
```

`conftest.py` contiene las fixtures compartidas de pytest, incluyendo:

- cliente de FastAPI
- limpieza automática de la base de datos antes de cada test
- creación de un usuario autenticado
- generación automática de cabeceras `Authorization` mediante `auth_headers`
- segundo usuario autenticado mediante `second_auth_headers`

Los tests se distribuyen de la siguiente forma:

- `test_tasks_crud.py`: operaciones CRUD y validaciones de tareas
- `test_tasks_authorization.py`: autenticación, propiedad y aislamiento entre usuarios
- `test_tasks_filters.py`: paginación, filtros y validación de parámetros
- `test_users.py`: registro, duplicados, conflictos de integridad y validaciones de usuarios
- `test_auth.py`: login, generación de JWT, autenticación y casos límite de tokens
- `test_health.py`: comprobación del endpoint de estado de la API
- `conftest.py`: configuración y fixtures compartidas

Ejecutar todos los tests:

```bash
python -m pytest
```

Actualmente el proyecto cuenta con **39 tests automatizados**.

Entre otros comportamientos, la suite comprueba:

- CRUD completo de tareas
- autenticación JWT
- acceso con token inválido o expirado
- cabecera `WWW-Authenticate: Bearer`
- tareas inexistentes
- validación de IDs
- validación de títulos
- registro de usuarios
- validación de emails
- contraseñas inválidas
- emails duplicados
- manejo de `IntegrityError`
- recuperación de la sesión mediante `rollback()`
- login correcto e incorrecto
- JWT válido asociado a un usuario inexistente
- propiedad de tareas
- aislamiento entre usuarios
- paginación
- filtros por estado
- validación de parámetros
- healthcheck

### Cobertura de tests

La cobertura del código de aplicación se mide mediante `pytest-cov`.

Ejecutar tests y mostrar la cobertura:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

El reporte indica:

- número de líneas ejecutables por archivo
- líneas que no han sido ejecutadas por los tests
- porcentaje de cobertura
- líneas concretas que faltan por cubrir

Actualmente la suite alcanza:

```text
39 tests passed
100% coverage
```

sobre las líneas ejecutables del directorio `app/`.

El 100% de cobertura indica que todas las líneas ejecutables de la aplicación son recorridas al menos una vez por la suite actual. No implica por sí solo ausencia de errores, por lo que la cobertura se utiliza junto con tests funcionales y casos límite.

## Calidad de código

El proyecto utiliza Ruff para analizar el código y detectar problemas de estilo, imports y posibles errores.

Ejecutar Ruff:

```bash
ruff check .
```

Aplicar automáticamente correcciones seguras detectadas por Ruff:

```bash
ruff check . --fix
```

Antes de realizar commits importantes se recomienda ejecutar:

```bash
ruff check .
python -m pytest
```

Para una revisión completa incluyendo cobertura:

```bash
ruff check .
python -m pytest --cov=app --cov-report=term-missing
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

La integración de la cobertura de tests en el workflow de CI se realizará en la fase final de configuración de GitHub Actions.

## Próximas mejoras

- Integración de cobertura en GitHub Actions
- Revisión final de CI
- Deploy en Azure
- Revisión de secretos y configuración para producción
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
- validación de access tokens JWT
- identificación del usuario mediante el claim `sub`
- expiración de tokens mediante el claim `exp`
- obtención del usuario autenticado mediante JWT
- rechazo de JWT válidos asociados a usuarios inexistentes
- endpoint protegido `GET /auth/me`
- protección JWT de todos los endpoints `/tasks`
- cabecera `WWW-Authenticate: Bearer` en errores de autenticación
- mismo mensaje de error ante email inexistente o contraseña incorrecta en login
- relación entre tareas y usuarios mediante `user_id`
- foreign key `tasks.user_id → users.id`
- índice sobre `tasks.user_id`
- asignación automática del propietario de una tarea desde el JWT
- aislamiento completo de tareas entre usuarios
- listado de tareas filtrado por usuario autenticado
- protección de consulta de tareas ajenas
- protección de modificación de tareas ajenas
- protección de eliminación de tareas ajenas
- uso de `404` para evitar revelar recursos pertenecientes a otros usuarios
- paginación mediante `skip` y `limit`
- límite máximo de 100 tareas por petición
- filtrado por estado `completed`
- validación de parámetros de paginación
- validación de IDs de tareas positivos
- validación de longitud de títulos y contraseñas
- endpoint público `GET /health`
- protección frente a emails duplicados mediante comprobación previa y restricción `UNIQUE`
- respuesta `409 Conflict` para emails duplicados
- manejo de `IntegrityError` y `rollback()` de la sesión
- migraciones y versionado de base de datos con Alembic
- migraciones reproducibles desde una base de datos vacía
- configuración centralizada con `pydantic-settings`
- configuración JWT mediante variables de entorno
- organización de rutas mediante routers
- base de datos de test separada
- suite de tests reorganizada por responsabilidad
- fixtures compartidas mediante `conftest.py`
- fixtures `auth_headers` y `second_auth_headers`
- limpieza automática de la base de datos entre tests
- tests de aislamiento entre múltiples usuarios
- tests de paginación, filtros, autenticación y casos límite
- manejo de errores de integridad cubierto mediante tests
- 39 tests automáticos
- cobertura del 100% sobre `app/`
- análisis de código con Ruff
- contenerización de FastAPI mediante Docker
- PostgreSQL ejecutado mediante Docker Compose
- comunicación interna entre API y PostgreSQL mediante el servicio `db`
- healthcheck de PostgreSQL
- ejecución automática de las migraciones Alembic antes de iniciar FastAPI
- persistencia de los datos mediante volumen Docker
- recreación de contenedores sin pérdida de usuarios ni tareas
- CI con GitHub Actions, PostgreSQL y migraciones

La siguiente fase estará centrada en completar la integración continua con cobertura y realizar las últimas validaciones de CI antes del despliegue en Azure.