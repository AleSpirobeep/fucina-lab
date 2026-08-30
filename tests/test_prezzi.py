from decimal import Decimal

import pytest

from listino import (
    aggiungi_iva,
    applica_sconto,
    arrotonda,
    totale_documento,
    totale_riga,
)


class TestArrotonda:
    def test_arrotonda_a_due_decimali(self):
        assert arrotonda(Decimal("1.005")) == Decimal("1.01")

    def test_half_up_non_half_even(self):
        # La regola bancaria darebbe 2.02; quella commerciale dà 2.03.
        assert arrotonda(Decimal("2.025")) == Decimal("2.03")

    def test_importo_gia_tondo_resta_invariato(self):
        assert arrotonda(Decimal("10.00")) == Decimal("10.00")


class TestApplicaSconto:
    def test_sconto_semplice(self):
        assert applica_sconto(Decimal("100"), Decimal("10")) == Decimal("90.00")

    def test_sconto_decimale(self):
        assert applica_sconto(Decimal("80"), Decimal("12.5")) == Decimal("70.00")

    def test_sconto_zero_non_cambia_nulla(self):
        assert applica_sconto(Decimal("33.33"), Decimal("0")) == Decimal("33.33")

    def test_sconto_totale(self):
        assert applica_sconto(Decimal("50"), Decimal("100")) == Decimal("0.00")

    @pytest.mark.parametrize("sconto", [Decimal("-1"), Decimal("101")])
    def test_sconto_fuori_intervallo(self, sconto):
        with pytest.raises(ValueError, match="fuori intervallo"):
            applica_sconto(Decimal("100"), sconto)


class TestAggiungiIva:
    def test_aliquota_ordinaria(self):
        assert aggiungi_iva(Decimal("100")) == Decimal("122.00")

    def test_aliquota_ridotta(self):
        assert aggiungi_iva(Decimal("100"), "ridotta") == Decimal("110.00")

    def test_aliquota_minima(self):
        assert aggiungi_iva(Decimal("250"), "minima") == Decimal("260.00")

    def test_aliquota_sconosciuta(self):
        with pytest.raises(ValueError, match="aliquota sconosciuta"):
            aggiungi_iva(Decimal("100"), "agevolata")


class TestTotaleRiga:
    def test_riga_semplice(self):
        assert totale_riga(Decimal("10"), 3) == Decimal("36.60")

    def test_riga_con_sconto(self):
        assert totale_riga(Decimal("10"), 10, Decimal("20")) == Decimal("97.60")

    def test_quantita_zero(self):
        assert totale_riga(Decimal("19.99"), 0) == Decimal("0.00")

    def test_quantita_negativa(self):
        with pytest.raises(ValueError, match="quantità negativa"):
            totale_riga(Decimal("10"), -1)


class TestTotaleDocumento:
    def test_documento_vuoto(self):
        assert totale_documento([]) == Decimal("0.00")

    def test_documento_multiriga(self):
        righe = [
            {"prezzo_unitario": Decimal("10"), "quantita": 3},
            {"prezzo_unitario": Decimal("5"), "quantita": 2, "aliquota": "ridotta"},
            {
                "prezzo_unitario": Decimal("100"),
                "quantita": 1,
                "sconto_percentuale": Decimal("15"),
            },
        ]
        # 36.60 + 11.00 + 103.70
        assert totale_documento(righe) == Decimal("151.30")
