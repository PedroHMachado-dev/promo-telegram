import os
import sys
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    print("❌ Preencha API_ID e API_HASH no seu arquivo .env antes de rodar este script.")
    sys.exit(1)

print("=" * 65)
print("🔑 GERADOR DE SESSÃO DO TELEGRAM (TELEGRAM_SESSION_STRING)")
print("=" * 65)
print("Este script vai autenticar com sua conta do Telegram e gerar")
print("uma chave de texto segura para rodar no Render sem pedir login.")
print("=" * 65)

try:
    with TelegramClient(StringSession(), int(API_ID), API_HASH) as client:
        session_string = client.session.save()
        print("\n" + "=" * 65)
        print("✅ SESSÃO GERADA COM SUCESSO!")
        print("=" * 65)
        print("\nCopie o código abaixo (uma única linha, sem espaços adicionais):\n")
        print(session_string)
        print("\n" + "=" * 65)
        print("Guarde este código. Você vai colocá-lo no Render na variável:")
        print("TELEGRAM_SESSION_STRING")
        print("=" * 65)
except Exception as error:
    print(f"\n❌ Erro ao gerar sessão: {error}")
