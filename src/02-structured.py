import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the response formet in a pydantic model


class CalendarEvent(BaseModel):
    name: str
    date: str
    time: str
    duration: str
    participants: list[str]


# call the model

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract the event information from the text."},
        {
            "role": "user",
            "content": "Bastiaan, Mark and Michael are meeting at noon 12th of October to discuss the project for 2 hours.",
        },
    ],
    response_format=CalendarEvent,
)

#  Parse the response

event = completion.choices[0].message.parsed
event.name
event.date
event.time
event.duration
event.participants
