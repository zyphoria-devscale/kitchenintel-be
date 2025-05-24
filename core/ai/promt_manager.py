import json
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from shared.utils import graph_data

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)


class PromptManager:
    def __init__(self, messages=None, model="o4-mini"):
        if messages is None:
            messages = []
        self.messages = messages
        self.model = model

    def add_system_message(self, text: str):
        self.messages.append({"role": "system", "content": text})

    def add_message_with_image(self, role, text: str, image_url: str):
        self.messages.append(
            {
                "role": role,
                "content": [
                    {
                        "type": "text",
                        "text": text,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    }
                ]
            }
        )

    def add_message_with_images(self, text: str, graphs: List[graph_data]):
        content = [{
            "type": "text",
            "text": text,
        }]
        for graph in graphs:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": graph.url,
                    },
                },
            )
            content.append(
                {
                    "type": "text",
                    "text": graph.description,
                },
            )
        self.messages.append({"role": "user", "content": content})

    def add_message(self, role, text: str):
        self.messages.append({"role": role, "content": text})

    def set_messages(self, messages):
        self.messages = messages

    def get_messages(self):
        return self.messages

    def generate(self):
        response = client.chat.completions.create(
            model=self.model, messages=self.messages
        )
        return response.choices[0].message.content

    def generate_structured(self, schema):
        response = client.beta.chat.completions.parse(
            model=self.model, messages=self.messages, response_format=schema
        )

        result = response.choices[0].message.model_dump()
        content = json.loads(result["content"])
        return content
