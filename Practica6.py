import aiohttp
import asyncio
import random
import re
import tkinter as tk
from tkinter import scrolledtext

API_KEY = "uiQPCX1uoa9C8q+O6SfG4Q==2arb9y9pNjVIwLBz"
HEADERS = {"X-Api-Key": API_KEY}

JOKES_API_URL = "https://api.api-ninjas.com/v1/jokes"
EMOJI_API_URL = "https://api.api-ninjas.com/v1/emoji?name="

# --- Асинхронные функции ---

async def fetch_joke(session):
    async with session.get(JOKES_API_URL, headers=HEADERS) as response:
        data = await response.json()
        return data[0]['joke'] if data else "Шутка не найдена."

async def fetch_emoji(session, keyword):
    async with session.get(EMOJI_API_URL + keyword, headers=HEADERS) as response:
        data = await response.json()
        if data:
            return data[0]['character']
        return None

def insert_emoji(joke, keyword, emoji):
    pattern = re.compile(rf'\b({re.escape(keyword)})\b', re.IGNORECASE)
    return pattern.sub(r'\1 ' + emoji, joke, count=1)

# --- GUI + интеграция с asyncio ---

def run_gui():
    window = tk.Tk()
    window.title("Генератор шуток 🤡")
    window.geometry("600x300")

    label = tk.Label(window, text="Нажми кнопку, чтобы получить шутку!", font=("Arial", 14))
    label.pack(pady=10)

    output = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12), height=6, width=70)
    output.pack(pady=10)

    async def generate_joke():
        async with aiohttp.ClientSession() as session:
            joke = await fetch_joke(session)
            words = joke.split()
            keyword = random.choice(words).strip('.,!?').lower()
            emoji = await fetch_emoji(session, keyword)
            joke_with_emoji = insert_emoji(joke, keyword, emoji) if emoji else joke
            output.delete('1.0', tk.END)
            output.insert(tk.END, f"🗯 Оригинал:\n{joke}\n\n🎉 С эмодзи:\n{joke_with_emoji}")

    def on_click():
        asyncio.create_task(generate_joke())

    button = tk.Button(window, text="Получить шутку", command=on_click, font=("Arial", 12))
    button.pack(pady=10)

    # Поддержка asyncio в Tkinter
    async def tkinter_loop():
        while True:
            window.update()
            await asyncio.sleep(0.05)

    asyncio.run(tkinter_loop())

if __name__ == "__main__":
    run_gui()