from webparser import WebContentParser  # Fix the module name
from vacancyagent import VacancyParser


def run():
    web_parser = WebContentParser()
    vacancy_parser = VacancyParser()

    url = "https://unjobs.org/vacancies/1738685020313"

    # First get the content from the web
    web_content = web_parser.get_vacancy_announcement(url)

    # Then parse it with the AI
    try:
        vacancy = vacancy_parser.parse_vacancy(url, web_content["content"])
        print(vacancy)
    except ValueError as e:
        print(f"Failed to parse vacancy: {e}")


# Example usage:

if __name__ == "__main__":
    run()
