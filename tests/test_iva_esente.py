from decimal import Decimal

import pytest

from listino import aggiungi_iva, totale_riga


class TestAliquotaEsente:
    def test_esente_con_causale_non_applica_iva(self):
        assert aggiungi_iva(
            Decimal("100"), "esente", "art. 10 DPR 633/72"
        ) == Decimal("100.00")

    def test_esente_senza_causale_solleva_valueerror(self):
        with pytest.raises(ValueError, match="causale"):
            aggiungi_iva(Decimal("100"), "esente")

    def test_esente_con_causale_vuota_solleva_valueerror(self):
        with pytest.raises(ValueError, match="causale"):
            aggiungi_iva(Decimal("100"), "esente", "")

    def test_totale_riga_esente_pari_a_imponibile_scontato(self):
        totale = totale_riga(
            Decimal("50"),
            2,
            Decimal("10"),
            aliquota="esente",
            causale_esenzione="art. 10 DPR 633/72",
        )
        assert totale == Decimal("90.00")

    def test_totale_riga_esente_senza_causale_solleva_valueerror(self):
        with pytest.raises(ValueError, match="causale"):
            totale_riga(Decimal("50"), 2, aliquota="esente")


class TestAliquoteEsistentiInvariate:
    def test_aliquota_ordinaria_non_richiede_causale(self):
        assert aggiungi_iva(Decimal("100")) == Decimal("122.00")

    def test_aliquota_ridotta_non_richiede_causale(self):
        assert aggiungi_iva(Decimal("100"), "ridotta") == Decimal("110.00")
