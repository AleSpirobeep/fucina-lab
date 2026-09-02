---
status: accepted
date: 2026-09-02
decision-makers: [dev-agent]
---
# Sconto a valore fisso: nuova funzione invece di un parametro

## Contesto e problema

`applica_sconto` accetta solo uno sconto percentuale. La issue #1 chiede di poter
applicare anche uno sconto a valore assoluto (es. 5,00 EUR su un imponibile di
80,00 EUR), lasciando aperta la scelta fra una nuova funzione o un parametro
aggiuntivo sulla funzione esistente.

## Opzioni considerate

- **Parametro su `applica_sconto`** (es. `tipo="percentuale"|"valore"`, oppure due
  parametri opzionali mutuamente esclusivi): un solo punto d'ingresso, ma la firma
  della funzione diventa ambigua (quale parametro vale se sono passati entrambi?)
  e i 19 test esistenti chiamano `applica_sconto` posizionalmente assumendo che il
  secondo argomento sia sempre una percentuale.
- **Nuova funzione `applica_sconto_valore`**: firma semplice e simmetrica a
  `applica_sconto`, nessun rischio di cambiare il comportamento della funzione
  esistente, nessuna modifica ai test esistenti.

## Decisione

Aggiunta la funzione `applica_sconto_valore(imponibile, sconto_valore)` in
`listino/prezzi.py`, esportata da `listino/__init__.py`. Solleva `ValueError` se
lo sconto è negativo o supera l'imponibile; il risultato passa da `arrotonda`
(half up, due decimali), come le altre funzioni del modulo.

## Conseguenze

`applica_sconto` resta invariata: nessun rischio per il codice o i test esistenti.
Chi vuole scontare a valore chiama la nuova funzione invece di passare una
percentuale calcolata a mano. `totale_riga` continua a usare solo lo sconto
percentuale; un eventuale supporto allo sconto a valore in `totale_riga` non è
richiesto dalla issue e non è stato aggiunto.
