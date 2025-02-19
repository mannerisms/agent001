import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-4",  # Fixed model name from "gpt-4o"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "write me a limerick about python programming"},
    ],
)

response = completion.choices[0].message.content  # Fixed message access syntax
print(response)
