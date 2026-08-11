import re


def encontrar_produtos(texto, produtos):

    texto_normalizado = texto.lower()

    encontrados = []

    for nome_produto, configuracao in produtos.items():

        palavras_chave = configuracao["palavras_chave"]

        for palavra in palavras_chave:

            if palavra.lower() in texto_normalizado:

                encontrados.append(nome_produto)

                break

    return encontrados


def encontrar_precos(texto):

    # Aceita qualquer quantidade de dígitos, com ou sem separadores de milhar.
    # Exemplos: R$ 99,90; R$ 1343; R$ 1.343,00; R$ 123456,78.
    padrao = r'(?:R\$|RS)\s*(\d+(?:\.\d{3})*(?:,\d{1,2})?)'

    resultados = re.findall(
        padrao,
        texto,
        re.IGNORECASE
    )

    precos = []

    for valor in resultados:

        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")

        try:

            precos.append(float(valor))

        except ValueError:

            pass

    return precos


def encontrar_links(texto):

    links_markdown = re.findall(
        r'\]\((https?://[^\s\)]+)\)',
        texto
    )

    if links_markdown:
        return links_markdown

    links = re.findall(
        r'https?://[^\s\)\]]+',
        texto
    )

    return links


def encontrar_preco_promocional(texto):

    padrao = (
        r'(?:por|preço|preco)'
        r'\s*:?\s*'
        r'(?:R\$|RS)'
        r'\s*'
        r'(\d+(?:\.\d{3})*(?:,\d{2})?)'
    )

    resultado = re.search(
        padrao,
        texto,
        re.IGNORECASE
    )

    if not resultado:
        return None

    valor = resultado.group(1)

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    try:
        return float(valor)

    except ValueError:
        return None


def encontrar_preco_anterior(texto):

    padrao = (
        r'de\s+(?:R\$|RS)\s*'
        r'(\d+(?:\.\d{3})*(?:,\d{2})?)'
    )

    resultado = re.search(
        padrao,
        texto,
        re.IGNORECASE
    )

    if not resultado:
        return None

    valor = resultado.group(1)

    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    try:
        return float(valor)

    except ValueError:
        return None


def verificar_preco_maximo(produto, preco, produtos):

    preco_maximo = produtos[produto]["preco_maximo"]

    return preco <= preco_maximo


def calcular_desconto(preco_anterior, preco_atual):

    if preco_anterior is None or preco_atual is None:
        return None

    if preco_anterior <= 0:
        return None

    economia = preco_anterior - preco_atual

    desconto = (economia / preco_anterior) * 100

    return economia, desconto
