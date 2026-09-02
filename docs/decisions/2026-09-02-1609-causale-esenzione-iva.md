---
status: accepted
date: 2026-09-02
decision-makers: [dev-agent]
---
# Causale obbligatoria per l'aliquota IVA esente

## Contesto e problema

L'issue #3 chiede un'aliquota IVA a zero per le operazioni esenti, ma uno 0
nell'aliquota non basta: in fattura va stampata anche la causale
dell'esenzione (es. il riferimento normativo). Serve quindi un modo per
imporre che la causale sia sempre presente quando si usa l'aliquota esente,
senza cambiare il comportamento delle aliquote esistenti.

## Opzioni considerate

1. Modellare "esente" come una stringa a parte, fuori da `ALIQUOTE_IVA`,
   gestita con un ramo `if` dedicato in `aggiungi_iva`.
2. Aggiungere `"esente": Decimal("0")` a `ALIQUOTE_IVA` e aggiungere un
   parametro opzionale `causale_esenzione` a `aggiungi_iva` e `totale_riga`,
   validato solo quando l'aliquota è `"esente"`.

## Decisione

Opzione 2. `"esente"` resta un'aliquota come le altre (stessa validazione,
stesso messaggio d'errore per aliquote sconosciute), così le aliquote
esistenti non cambiano comportamento. Il nuovo parametro `causale_esenzione`
è opzionale per non rompere le chiamate esistenti, ma `aggiungi_iva` solleva
`ValueError` se l'aliquota è `"esente"` e la causale è assente o vuota.

La causale non viene memorizzata né restituita da queste funzioni: il modulo
`listino.prezzi` calcola importi, non stampa fatture. La stampa della
causale in fattura resta compito di un livello successivo, non ancora
presente in questo repository.

## Conseguenze

- Le firme di `aggiungi_iva` e `totale_riga` guadagnano un parametro opzionale
  in coda; le chiamate posizionali esistenti restano valide.
- Chi userà l'aliquota esente dovrà passare esplicitamente una causale non
  vuota, altrimenti ottiene un `ValueError` chiaro.
- Se in futuro serve stampare la causale in fattura, andrà propagata da un
  livello superiore che oggi non esiste in questo repo.
