import asyncio
import os
import sys
import threading
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

from api import run as run_api
from monitor_test import iniciar_monitor


def main():
    print("=" * 65)
    print("🚀 INICIANDO SERVIÇO UNIFICADO (API + MONITOR)")
    print("=" * 65)

    # Inicia a API HTTP em uma thread separada
    print("📡 Iniciando servidor HTTP da API...")
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # Inicia o Monitor Telethon no loop assíncrono principal
    print("🤖 Iniciando Monitor do Telegram...")
    try:
        asyncio.run(iniciar_monitor())
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Servidor encerrado.")


if __name__ == "__main__":
    main()
