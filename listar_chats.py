from telethon import TelegramClient
import os

from dotenv import load_dotenv


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


client = TelegramClient(
    "telegram_session",
    API_ID,
    API_HASH
)


async def main():

    print()
    print("=" * 70)
    print("📱 CHATS DISPONÍVEIS")
    print("=" * 70)

    async for dialog in client.iter_dialogs():

        print(
            f"ID: {dialog.id} | "
            f"Nome: {dialog.name}"
        )

    print("=" * 70)


with client:

    client.loop.run_until_complete(main())