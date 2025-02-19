from pydantic import BaseModel


class Vacancy(BaseModel):
    url: str
    title: str
    role: str
    location: str
    description: str
    responsibilities: list[str]
    requirements: list[str]
    deadline: str
    salary: str
    level: str
