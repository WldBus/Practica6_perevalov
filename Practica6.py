import aiohttp
import asyncio
import random
import re

API_KEY = "uiQPCX1uoa9C8q+O6SfG4Q==2arb9y9pNjVIwLBz"
HEADERS = {"X-Api-Key": API_KEY}

JOKES_API_URL = "https://api.api-ninjas.com/v1/jokes"
EMOJI_API_URL = "https://api.api-ninjas.com/v1/emoji?name="

async def fetch_joke(session):
    async with session.get(JOKES_API_URL, headers=HEADERS) as response:
        data = await response.json()
        return data[0]['joke'] if data else "No joke found."

async def fetch_emoji(session, keyword):
    async with session.get(EMOJI_API_URL + keyword, headers=HEADERS) as response:
        data = await response.json()
        if data:
            return data[0]['character']
        return None

def insert_emoji(joke, keyword, emoji):
    # Ищем первое вхождение ключевого слова (не чувствительно к регистру)
    pattern = re.compile(rf'\b({re.escape(keyword)})\b', re.IGNORECASE)
    return pattern.sub(r'\1 ' + emoji, joke, count=1)

async def main():
    async with aiohttp.ClientSession() as session:
        joke = await fetch_joke(session)
        print(f"\n🗯 Оригинальная шутка:\n{joke}")

        words = joke.split()
        keyword = random.choice(words).strip('.,!?').lower()

        emoji = await fetch_emoji(session, keyword)
        if emoji:
            joke_with_emoji = insert_emoji(joke, keyword, emoji)
            print(f"\n🎯 Ключевое слово: '{keyword}'")
            print(f"🎉 Итоговая шутка с эмодзи:\n{joke_with_emoji}")
        else:
            print(f"\n😅 Не удалось найти эмодзи для слова '{keyword}'. Вот просто шутка:\n{joke}")

if __name__ == "__main__":
    asyncio.run(main())