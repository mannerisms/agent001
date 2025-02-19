import os
from typing import Optional
from openai import OpenAI
from models import Vacancy


class VacancyParser:
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """
        Extract the following information from the vacancy announcement:
        - Organization and title
        - Role (max 3 words)
        - Location (city)
        - Level
        - Salary
        - Deadline (format: dd/mm/yyyy)
        - List of responsibilities
        - List of requirements

        Return empty string if information is not available.
        """

    def parse_vacancy(self, url: str, vacancy_text: str) -> Vacancy:
        """
        Parse vacancy text using OpenAI's model and return structured data.

        Args:
            url (str): The URL of the vacancy
            vacancy_text (str): The raw vacancy text to parse

        Returns:
            Vacancy: Structured vacancy data

        Raises:
            ValueError: If the API call fails or returns invalid data
        """
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": vacancy_text},
                ],
                response_format=Vacancy,
            )

            parsed_data = completion.choices[0].message.content
            return Vacancy(**parsed_data, url=url)

        except Exception as e:
            raise ValueError(f"Failed to parse vacancy: {str(e)}")
