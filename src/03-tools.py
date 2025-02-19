import os

from openai import OpenAI
from pydantic import BaseModel
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the response formet in a pydantic model


class VacancyAnnouncement(BaseModel):
    url: str
    title: str
    role: str
    location: str
    deadline: str
    description: str
    requirements: list[str]
    level: str


url = "https://unjobs.org/vacancies/1738685020313"


# get the vacancy announcement from the website
def get_vacancy_announcement(url: str):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text


vacancy = get_vacancy_announcement(url)
