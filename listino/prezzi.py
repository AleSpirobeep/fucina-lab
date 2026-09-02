"""Calcolo di importi di listino: sconti, IVA, totali.

Tutti gli importi sono Decimal. Non usare float: su denaro produce errori
di arrotondamento che si accumulano riga dopo riga.
"""

from decimal import Decimal, ROUND_HALF_UP

ALIQUOTE_IVA = {
    "ordinaria": Decimal("0.22"),
    "ridotta": Decimal("0.10"),
    "minima": Decimal("0.04"),
    "esente": Decimal("0"),
}

CENTESIMO = Decimal("0.01")


def arrotonda(importo: Decimal) -> Decimal:
    """Arrotonda a due decimali con la regola commerciale (half up)."""
    return Decimal(importo).quantize(CENTESIMO, rounding=ROUND_HALF_UP)


def applica_sconto(imponibile: Decimal, sconto_percentuale: Decimal) -> Decimal:
    """Applica uno sconto percentuale a un imponibile.

    Lo sconto è espresso in punti percentuali: 12.5 significa 12,5%.
    """
    imponibile = Decimal(imponibile)
    sconto = Decimal(sconto_percentuale)
    if sconto < 0 or sconto > 100:
        raise ValueError(f"sconto fuori intervallo 0-100: {sconto}")
    return arrotonda(imponibile * (Decimal(100) - sconto) / Decimal(100))


def _valida_aliquota(aliquota: str, causale_esenzione: str | None) -> None:
    if aliquota not in ALIQUOTE_IVA:
        raise ValueError(
            f"aliquota sconosciuta: {aliquota!r}; ammesse {sorted(ALIQUOTE_IVA)}"
        )
    if aliquota == "esente" and not causale_esenzione:
        raise ValueError("operazione esente senza causale: la causale è obbligatoria")


def aggiungi_iva(
    imponibile: Decimal,
    aliquota: str = "ordinaria",
    causale_esenzione: str | None = None,
) -> Decimal:
    """Somma l'IVA a un imponibile, data un'aliquota nota.

    L'aliquota "esente" richiede una causale (es. il riferimento normativo),
    perché in fattura va stampata: uno 0 nell'aliquota da solo non basta.
    """
    _valida_aliquota(aliquota, causale_esenzione)
    imponibile = Decimal(imponibile)
    return arrotonda(imponibile * (Decimal(1) + ALIQUOTE_IVA[aliquota]))


def _totale_riga_esatto(
    prezzo_unitario: Decimal,
    quantita: int,
    sconto_percentuale: Decimal = Decimal(0),
    aliquota: str = "ordinaria",
    causale_esenzione: str | None = None,
) -> Decimal:
    """Totale IVA inclusa di una riga, senza arrotondare il risultato finale.

    Usato da `totale_documento` in modalità "per_documento": serve l'importo
    esatto di riga, non ancora arrotondato a due decimali.
    """
    if quantita < 0:
        raise ValueError(f"quantità negativa: {quantita}")
    _valida_aliquota(aliquota, causale_esenzione)
    imponibile = Decimal(prezzo_unitario) * Decimal(quantita)
    scontato = applica_sconto(imponibile, sconto_percentuale)
    return scontato * (Decimal(1) + ALIQUOTE_IVA[aliquota])


def totale_riga(
    prezzo_unitario: Decimal,
    quantita: int,
    sconto_percentuale: Decimal = Decimal(0),
    aliquota: str = "ordinaria",
    causale_esenzione: str | None = None,
) -> Decimal:
    """Totale IVA inclusa di una riga di documento."""
    return arrotonda(
        _totale_riga_esatto(
            prezzo_unitario, quantita, sconto_percentuale, aliquota, causale_esenzione
        )
    )


MODALITA_ARROTONDAMENTO = ("per_riga", "per_documento")


def totale_documento(
    righe: list[dict], modalita_arrotondamento: str = "per_riga"
) -> Decimal:
    """Somma i totali delle righe di un documento.

    Ogni riga è un dizionario con le chiavi accettate da totale_riga.

    `modalita_arrotondamento`:
    - "per_riga" (default): arrotonda ogni riga a due decimali e poi somma.
      È il comportamento storico di questa funzione: non rompe chi già la
      chiama senza specificare la modalità.
    - "per_documento": somma gli importi esatti (non arrotondati) delle
      righe e arrotonda solo il totale finale.

    Le due modalità possono differire di qualche centesimo sui documenti
    con molte righe, perché gli arrotondamenti di riga si accumulano.
    """
    if modalita_arrotondamento not in MODALITA_ARROTONDAMENTO:
        raise ValueError(
            f"modalità di arrotondamento sconosciuta: {modalita_arrotondamento!r}; "
            f"ammesse {MODALITA_ARROTONDAMENTO}"
        )
    if modalita_arrotondamento == "per_documento":
        return arrotonda(
            sum((_totale_riga_esatto(**riga) for riga in righe), Decimal(0))
        )
    return arrotonda(sum((totale_riga(**riga) for riga in righe), Decimal(0)))
