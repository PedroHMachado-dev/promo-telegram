import os
import sys
import asyncio

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from main import analisar_promocao
from notifier import validar_configuracao_notificacao
from storage import load_data, save_telegram_groups


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


load_dotenv()


def obter_cliente():
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")

    if not api_id or not api_hash:
        raise RuntimeError("Preencha API_ID e API_HASH no arquivo .env")

    validar_configuracao_notificacao()

    session_str = os.getenv("TELEGRAM_SESSION_STRING", "").strip()
    session = StringSession(session_str) if session_str else "telegram_session"

    return TelegramClient(session, int(api_id), api_hash)


client = obter_cliente()


async def sincronizar_grupos_telegram(cli=None):
    c = cli or client
    try:
        dialogs = await c.get_dialogs()
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


async def sincronizar_periodicamente(cli=None):
    while True:
        await asyncio.sleep(60)
        await sincronizar_grupos_telegram(cli)


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


async def iniciar_monitor():
    print("==============================================")
    print("🤖 MONITOR DE PROMOÇÕES INICIADO")
    print("==============================================")
    grupos_iniciais = load_data().get("groups", [])
    print(f"Grupos monitorados: {len(grupos_iniciais)}")
    for grupo in grupos_iniciais:
        print(f"  - {grupo['name']} ({grupo['id']})")
    print("Aguardando novas mensagens...")
    print("==============================================")

    await client.start()
    await sincronizar_grupos_telegram()
    asyncio.create_task(sincronizar_periodicamente())
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(iniciar_monitor())
    except KeyboardInterrupt:
        print("\n🛑 Monitor finalizado.")
