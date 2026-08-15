import os
import sys
import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient, events

from main import analisar_promocao
from notifier import validar_configuracao_notificacao
from storage import load_data, save_telegram_groups


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


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


async def sincronizar_grupos_telegram():
    try:
        dialogs = await client.get_dialogs()
        grupos = []
        for dialog in dialogs:
            if not (dialog.is_group or dialog.is_channel):
                continue
            entity = dialog.entity
            grupos.append(
                {
                    "id": str(dialog.id),
                    "name": dialog.name or "Sem nome",
                    "type": "group" if dialog.is_group else "channel",
                    "username": getattr(entity, "username", None),
                }
            )

        grupos.sort(key=lambda grupo: grupo["name"].casefold())
        save_telegram_groups(grupos)
        print(f"🔄 Grupos disponíveis sincronizados: {len(grupos)}")
    except Exception as error:
        print(f"⚠️ Não foi possível sincronizar os grupos: {error}")


async def sincronizar_periodicamente():
    while True:
        await asyncio.sleep(60)
        await sincronizar_grupos_telegram()


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
client.loop.run_until_complete(sincronizar_grupos_telegram())
client.loop.create_task(sincronizar_periodicamente())
client.run_until_disconnected()
