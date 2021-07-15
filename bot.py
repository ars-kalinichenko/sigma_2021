import os

import requests
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer

API_TOKEN = os.environ.get("TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def fact():
    response = requests.get("https://catfact.ninja/fact")
    return response.json().get("fact", "Fact?")


def is_toxic(message):
    results = model.predict(message)[0]
    print(results)
    return results.get("negative", 1) > results.get("positive", 0)


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await message.reply(fact())


@dp.message_handler()
async def echo(message):
    toxic = is_toxic([message.text])  # -> True or False
    if toxic:
        await message.answer("You're toxic! 🥵")
    else:
        await message.answer("Nice! 😀")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
