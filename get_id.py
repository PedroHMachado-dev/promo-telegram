import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    print("\n================================")
    print("USUÁRIO ENCONTRADO")
    print("================================")

    print(f"Nome: {user.first_name}")
    print(f"Username: @{user.username}")
    print(f"ID: {user.id}")

    print("================================\n")

    await update.message.reply_text(
        f"Olá, {user.first_name}!\n\n"
        f"Seu ID do Telegram é:\n"
        f"`{user.id}`",
        parse_mode="Markdown"
    )


def main():

    application = Application.builder().token(
        BOT_TOKEN
    ).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    print("🤖 Bot iniciado...")
    print("Envie /start para o bot.")

    application.run_polling()


if __name__ == "__main__":
    main()