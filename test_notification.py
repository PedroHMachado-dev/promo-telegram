import asyncio

from notifier import enviar_promocao


async def main():

    await enviar_promocao(
        produto="RTX 4060 ASUS 8GB",
        preco_anterior=2499.90,
        preco_atual=1699.90,
        economia=800.00,
        desconto=32.0,
        link="https://www.exemplo.com/rtx4060"
    )


if __name__ == "__main__":
    asyncio.run(main())