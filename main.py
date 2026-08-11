
from filters import (
    encontrar_produtos,
    encontrar_precos,
    encontrar_links,
    encontrar_preco_promocional,
    encontrar_preco_anterior,
    verificar_preco_maximo,
    calcular_desconto
)

from notifier import enviar_promocao
from storage import add_promotion, products_for_filters


async def analisar_promocao(texto):

    PRODUTOS = products_for_filters()

    print("\n")
    print("=" * 60)
    print("🔎 ANALISANDO PROMOÇÃO")
    print("=" * 60)

    print("\n📩 Mensagem recebida:")
    print("-" * 60)

    print(texto)

    print("-" * 60)

    # =========================================================
    # PRODUTOS
    # =========================================================

    produtos = encontrar_produtos(
        texto,
        PRODUTOS
    )

    # =========================================================
    # PREÇOS
    # =========================================================

    precos = encontrar_precos(texto)

    # =========================================================
    # PREÇO ANTERIOR
    # =========================================================

    preco_anterior = encontrar_preco_anterior(texto)

    # =========================================================
    # PREÇO PROMOCIONAL
    # =========================================================

    preco_promocional = encontrar_preco_promocional(texto)

    # Muitos grupos publicam somente "R$ 999,90", sem escrever "por".
    # Nesses casos, o menor valor da mensagem é tratado como promocional.
    if preco_promocional is None and precos:
        preco_promocional = min(precos)

    # =========================================================
    # LINKS
    # =========================================================

    links = encontrar_links(texto)

    # =========================================================
    # PRODUTOS ENCONTRADOS
    # =========================================================

    print("\n📦 PRODUTOS ENCONTRADOS:")

    if produtos:

        for produto in produtos:
            print(f"   ✅ {produto}")

    else:

        print("   ❌ Nenhum produto encontrado")

    # =========================================================
    # PREÇOS
    # =========================================================

    print("\n💰 PREÇOS ENCONTRADOS:")

    if precos:

        for preco in precos:
            print(f"   • R$ {preco:.2f}")

    else:

        print("   ❌ Nenhum preço encontrado")

    # =========================================================
    # PREÇO ANTERIOR
    # =========================================================

    print("\n🏷️ PREÇO ANTERIOR:")

    if preco_anterior is not None:

        print(f"   R$ {preco_anterior:.2f}")

    else:

        print("   ❌ Não identificado")

    # =========================================================
    # PREÇO PROMOCIONAL
    # =========================================================

    print("\n🔥 PREÇO PROMOCIONAL:")

    if preco_promocional is not None:

        print(f"   R$ {preco_promocional:.2f}")

    else:

        print("   ❌ Não identificado")

    # =========================================================
    # LINKS
    # =========================================================

    print("\n🔗 LINKS:")

    if links:

        for link in links:
            print(f"   • {link}")

    else:

        print("   ❌ Nenhum link encontrado")

    # =========================================================
    # VERIFICAÇÃO
    # =========================================================

    if not produtos:

        print("\n❌ Nenhum produto monitorado.")
        return

    if preco_promocional is None:

        print("\n❌ Não foi possível identificar o preço promocional.")
        return

    if not links:

        print("\n❌ Nenhum link encontrado.")
        return

    # =========================================================
    # ANALISAR CADA PRODUTO
    # =========================================================

    for produto in produtos:

        preco_maximo = PRODUTOS[produto]["preco_maximo"]

        print("\n🎯 VERIFICAÇÃO DE PREÇO:")

        print(f"   Produto: {produto}")
        print(f"   Preço encontrado: R$ {preco_promocional:.2f}")
        print(f"   Preço máximo: R$ {preco_maximo:.2f}")

        # =====================================================
        # PREÇO ACIMA DO LIMITE
        # =====================================================

        if not verificar_preco_maximo(
            produto,
            preco_promocional,
            PRODUTOS
        ):

            print("   ❌ Acima do preço máximo.")
            print("   ⏭️ Promoção ignorada.")

            continue

        # =====================================================
        # CALCULAR DESCONTO
        # =====================================================

        resultado_desconto = calcular_desconto(
            preco_anterior,
            preco_promocional
        )

        if resultado_desconto:

            economia, desconto = resultado_desconto

        else:

            economia = 0
            desconto = 0

        # =====================================================
        # PROMOÇÃO APROVADA
        # =====================================================

        print("\n   🚨 DENTRO DO PREÇO!")
        print("   🔥 ALERTA DE PROMOÇÃO!")

        print(f"   💵 Economia: R$ {economia:.2f}")
        print(f"   📉 Desconto: {desconto:.1f}%")

        add_promotion(
            product=produto,
            previous_price=preco_anterior,
            current_price=preco_promocional,
            savings=economia,
            discount=desconto,
            link=links[0]
        )

        try:
            await enviar_promocao(
                produto=produto,
                preco_anterior=preco_anterior,
                preco_atual=preco_promocional,
                economia=economia,
                desconto=desconto,
                link=links[0]
            )
            print("\n📱 Notificação enviada para o Telegram!")
        except Exception as error:
            print(f"\n❌ Falha ao enviar notificação: {error}")


if __name__ == "__main__":
    from api import run

    run()
