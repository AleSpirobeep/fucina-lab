#!/usr/bin/env bash
# Crea le tre issue di collaudo. Da eseguire dentro il repo fucina-lab.
set -euo pipefail

gh issue create --title "Sconto a valore fisso oltre che percentuale" --body \
"applica_sconto accetta solo una percentuale. Serve poter applicare uno sconto
in valore assoluto, per esempio 5,00 EUR su un imponibile di 80,00 EUR.

Criteri di accettazione:
- una nuova funzione o un parametro permette lo sconto a valore
- uno sconto a valore superiore all'imponibile solleva ValueError
- il risultato resta arrotondato a due decimali, regola half up
- i 19 test esistenti restano verdi"

gh issue create --title "Aliquota IVA esente con causale obbligatoria" --body \
"Serve un'aliquota a zero per le operazioni esenti. In fattura la causale va
stampata, quindi non basta un0 nell'aliquota.

Criteri di accettazione:
- e possibile indicare un'operazione esente specificando una causale
- indicare l'esenzione senza causale solleva ValueError
- il totale di una riga esente e pari all'imponibile scontato
- le aliquote esistenti continuano a funzionare come prima"

gh issue create --title "Arrotondamento configurabile: per riga o per documento" --body \
"Oggi totale_documento arrotonda ogni riga e poi somma. Arrotondare invece solo il
totale produce risultati diversi di qualche centesimo su documenti lunghi.
Va reso configurabile.

Criteri di accettazione:
- totale_documento accetta una modalita di arrotondamento
- esiste un test che dimostra lo scostamento fra le due modalita
- il comportamento predefinito e documentato

Nota: quale delle due modalita debba essere il default non e stato deciso."

echo "Tre issue create."
