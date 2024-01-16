"""
combines langchain with chatgpt and chainlit
"""

# run with chainlit run main.py -w
# -w watches for changes in the codebase - good for debugging and dev.

# 3rd party libraries
import chainlit as cl
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_openai import ChatOpenAI

load_dotenv()  # take environment variables from .env e.g. OPENAI_API_KEY

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True, model= "gpt-3.5-turbo", temperature=1)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()