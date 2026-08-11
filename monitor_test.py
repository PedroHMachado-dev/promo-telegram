import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from main import analisar_promocao
from notifier import validar_configuracao_notificacao
from storage import load_data


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    raise RuntimeError("Preencha API_ID e API_HASH no arquivo .env")

validar_configuracao_notificacao()


client = TelegramClient(
    "telegram_session",
    API_ID,
    API_HASH
)


@client.on(events.NewMessage())
async def nova_mensagem(event):

    grupos = load_data().get("groups", [])
    ids_monitorados = {
        int(grupo["id"])
        for grupo in grupos
        if grupo.get("active", True)
    }

    if event.chat_id not in ids_monitorados:
        return

    mensagem = event.message.message

    print()
    print("=" * 70)
    print("📩 NOVA MENSAGEM RECEBIDA")
    print("=" * 70)

    print(mensagem)

    print("=" * 70)

    # Envia a mensagem para o nosso analisador
    await analisar_promocao(mensagem)


print("==============================================")
print("🤖 MONITOR DE PROMOÇÕES")
print("==============================================")
grupos_iniciais = load_data().get("groups", [])
print(f"Grupos monitorados: {len(grupos_iniciais)}")
for grupo in grupos_iniciais:
    print(f"  - {grupo['name']} ({grupo['id']})")
print("Aguardando novas mensagens...")
print("Pressione CTRL+C para parar.")
print("==============================================")


client.start()
client.run_until_disconnected()
