from fastapi import FastAPI

from app.routers import auth, tasks, users

app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/health", tags=["Health"])
def healthcheck():
    return {"status": "ok"}