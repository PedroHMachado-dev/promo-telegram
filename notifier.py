import os

from dotenv import load_dotenv
from telegram import Bot


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def validar_configuracao_notificacao():
    ausentes = [
        nome
        for nome, valor in {"BOT_TOKEN": BOT_TOKEN, "CHAT_ID": CHAT_ID}.items()
        if not valor
    ]
    if ausentes:
        raise RuntimeError(
            f"Preencha {', '.join(ausentes)} no arquivo .env para receber alertas"
        )


async def enviar_promocao(
    produto,
    preco_anterior,
    preco_atual,
    economia,
    desconto,
    link
):

    validar_configuracao_notificacao()

    preco_anterior_texto = (
        f"R$ {preco_anterior:.2f}"
        if preco_anterior is not None
        else "Não informado"
    )

    mensagem = (
        "🚨 PROMOÇÃO ENCONTRADA!\n\n"

        f"📦 Produto:\n"
        f"{produto}\n\n"

        f"💰 De:\n"
        f"{preco_anterior_texto}\n\n"

        f"🔥 Por:\n"
        f"R$ {preco_atual:.2f}\n\n"

        f"💵 Economia:\n"
        f"R$ {economia:.2f}\n\n"

        f"📉 Desconto:\n"
        f"{desconto:.1f}%\n\n"

        f"🔗 Comprar:\n"
        f"{link}"
    )

    async with Bot(token=BOT_TOKEN) as bot:

        await bot.send_message(
            chat_id=CHAT_ID,
            text=mensagem,
            disable_web_page_preview=False,
        )
