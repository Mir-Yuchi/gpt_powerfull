import openai_async
from data import config as cfg
import asyncio
from utils.db_api import database as db


async def ask(question, api_key, old):
    response = await openai_async.chat_complete(
        api_key,
        timeout=300,
        payload={
            "model": "gpt-3.5-turbo",
            "messages": old + [{"role": "user", "content": question}]
        },
    )
    crt = response.json()
    try:
        return crt["choices"][0]["message"]['content']
    except:
        if crt['error']['type'] == "insufficient_quota":
            db.delete_token_from_file(api_key)
        return 0


async def davinci(request, api_key, size):
    response = await openai_async.generate_img(
        api_key,
        timeout=200,
        payload={
            "prompt": request,
            "n": 1,
            "size": f"{size}x{size}"
        },
    )
    return response.json()["data"][0]["url"]
