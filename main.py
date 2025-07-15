import asyncio
import os
import logging
from aiogram import Bot
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # example: '@HodlerUz'

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

def get_top_10_coins():
    url = "https://api.coinpaprika.com/v1/tickers"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[:10]
        lines = []
        for i, coin in enumerate(data):
            name = coin["name"]
            symbol = coin["symbol"]
            price = coin["quotes"]["USD"]["price"]
            lines.append(f"{i+1}. <b>{name}</b> ({symbol}) – ${price:.2f}")
        lines.append("\n🔗 <a href='https://coinpaprika.com/'>Top 100 kurslar uchun bosing</a>")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Ma'lumot olishda xatolik: {e}"

async def send_daily_update():
    text = get_top_10_coins()
    try:
        await bot.send_message(CHANNEL_ID, text, disable_web_page_preview=True)
    except Exception as e:
        logging.error(f"Xabar yuborishda xatolik: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    scheduler.add_job(send_daily_update, trigger='cron', hour=8, minute=0)
    scheduler.add_job(send_daily_update, trigger='cron', hour=20, minute=0)
    scheduler.start()

    print("✅ Bot ishga tushdi. Kurslar har kuni 08:00 va 20:00 da yuboriladi.")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
