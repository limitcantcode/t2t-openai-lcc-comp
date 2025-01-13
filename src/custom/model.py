'''
Class implementing interface for AI T2T models running on OpenAI servers.

"model" will be one of OpenAI's models such as 'gpt-3.5-turbo' or a version
you've fine-tuned yourself (it will have a name like 'ft:gpt-4o-mini-2024-07-18:lcc:jaison:A92WIYvZ').
Please ensure you have your openai token in your ".env" as specified in the ".env-template"
'''
from openai import OpenAI
import logging

class OpenAIModel():
    def __init__(self, model_name):
        self.client = OpenAI()
        self.model_name = model_name

    def __call__(self, sys_prompt, user_prompt):
        messages=[
            { "role": "system", "content": sys_prompt },
            { "role": "user", "content": user_prompt }
        ]

        logging.debug(f"Sending messages: {messages}")
        stream = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            stream=True
        )

        logging.debug(f"Streaming results")
        full_response = ""
        for chunk in stream:
            content_chunk = chunk.choices[0].message.content or ""
            full_response += content_chunk
            yield content_chunk
        logging.debug(f"Finished with full response: {full_response}")