"""Test per la modalità di arrotondamento configurabile di totale_documento.

Vedi issue #5: arrotondare per riga o per documento produce risultati
diversi di qualche centesimo sui documenti con molte righe.
"""

from decimal import Decimal

import pytest

from listino.prezzi import totale_documento

RIGHE_DIVERGENTI = [
    {"prezzo_unitario": Decimal("0.01"), "quantita": 1, "aliquota": "ridotta"}
    for _ in range(7)
]


class TestModalitaArrotondamento:
    def test_default_e_per_riga(self):
        # Nessuna modalità specificata: comportamento storico, invariato.
        assert totale_documento(RIGHE_DIVERGENTI) == totale_documento(
            RIGHE_DIVERGENTI, "per_riga"
        )

    def test_scostamento_fra_le_due_modalita(self):
        # Ogni riga vale esattamente 0.011 (0.01 di imponibile + 10% di IVA),
        # che arrotondato per riga dà 0.01: sommando 7 righe si ottiene 0.07.
        # Sommando gli importi esatti si ottiene 0.077, che arrotondato una
        # sola volta dà 0.08.
        per_riga = totale_documento(RIGHE_DIVERGENTI, "per_riga")
        per_documento = totale_documento(RIGHE_DIVERGENTI, "per_documento")

        assert per_riga == Decimal("0.07")
        assert per_documento == Decimal("0.08")
        assert per_riga != per_documento

    def test_documento_vuoto_uguale_in_entrambe_le_modalita(self):
        assert totale_documento([], "per_riga") == Decimal("0.00")
        assert totale_documento([], "per_documento") == Decimal("0.00")

    def test_modalita_sconosciuta(self):
        with pytest.raises(ValueError, match="modalità di arrotondamento sconosciuta"):
            totale_documento(RIGHE_DIVERGENTI, "a_caso")
