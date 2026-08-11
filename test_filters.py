import unittest

from filters import encontrar_precos


class EncontrarPrecosTest(unittest.TestCase):
    def test_preco_com_mais_de_tres_digitos(self):
        self.assertEqual(encontrar_precos("💰 R$ 1343"), [1343.0])

    def test_preco_com_separador_de_milhar(self):
        self.assertEqual(encontrar_precos("Por R$ 1.343,90"), [1343.9])

    def test_preco_sem_limite_de_digitos(self):
        self.assertEqual(encontrar_precos("R$ 123456,78"), [123456.78])

    def test_varios_precos(self):
        self.assertEqual(
            encontrar_precos("De R$ 2.499,90 por R$ 1343"),
            [2499.9, 1343.0],
        )


if __name__ == "__main__":
    unittest.main()
