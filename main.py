# run with chainlit run main.py -w
import chainlit as cl
import openai
import os

api_key = os.environ.get('OPENAI_API_KEY')

@cl.on_message
async def main(message : str):
    await cl.Message(content=message).send()
