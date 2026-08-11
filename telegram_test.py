import os

from dotenv import load_dotenv
from telethon import TelegramClient


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


client = TelegramClient(
    "telegram_session",
    API_ID,
    API_HASH
)


async def main():

    me = await client.get_me()

    print()
    print("=" * 50)
    print("✅ TELEGRAM CONECTADO COM SUCESSO!")
    print("=" * 50)

    print(f"Nome: {me.first_name}")
    print(f"Username: @{me.username}")
    print(f"ID: {me.id}")

    print("=" * 50)


with client:

    client.loop.run_until_complete(main())