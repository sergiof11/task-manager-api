from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("El título no puede estar vacío")

        return value


class TaskCreate(TaskBase):
    completed: bool = False


class TaskUpdate(TaskBase):
    completed: bool


class Task(TaskBase):
    id: int
    completed: bool


class TaskDeleteResponse(TaskBase):
    message: str
    id: int
    completed: bool


class UserCreate(BaseModel):
    email: str
    password: str


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str