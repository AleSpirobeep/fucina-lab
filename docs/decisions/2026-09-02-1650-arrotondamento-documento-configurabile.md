---
status: accepted
date: 2026-09-02
decision-makers: [AleSpirobeep, dev-agent]
---
# Arrotondamento configurabile per riga o per documento

## Contesto e problema

`totale_documento` arrotondava sempre ogni riga (via `totale_riga`) e poi
sommava i risultati. Su documenti con molte righe questo si scosta di
qualche centesimo rispetto ad arrotondare una sola volta il totale finale,
sommando prima gli importi esatti delle righe. L'issue #5 chiede di rendere
la modalità configurabile, ma dichiara esplicitamente di non aver deciso
quale delle due debba essere il default: quella era la sola cosa da
chiarire con una persona, perché cambia l'importo che una chiamata già
esistente restituisce oggi.

## Opzioni considerate

1. Default `"per_riga"`: comportamento storico invariato per chi già chiama
   `totale_documento(righe)` senza specificare la modalità. Chi vuole
   l'arrotondamento per documento lo richiede esplicitamente.
2. Default `"per_documento"`: matematicamente più corretto (l'errore di
   arrotondamento non si accumula), ma cambia silenziosamente l'importo
   restituito dalle chiamate esistenti.

## Decisione

Opzione 1, scelta da AleSpirobeep nel thread dell'issue. `totale_documento`
accetta un nuovo parametro opzionale `modalita_arrotondamento`, con valori
ammessi `"per_riga"` (default) e `"per_documento"`. Il calcolo per riga
riusa `totale_riga`; il calcolo per documento usa una nuova funzione interna
`_totale_riga_esatto`, che condivide la stessa logica di sconto e IVA ma non
arrotonda il risultato finale della riga, cosicché la somma avvenga sugli
importi esatti prima dell'unico arrotondamento finale.

Lo sconto resta arrotondato in entrambe le modalità: è già un importo di
riga (il prezzo scontato) prima ancora di applicare l'IVA, non il totale di
cui parla l'issue.

## Conseguenze

- Nessuna rottura di compatibilità: le chiamate esistenti a
  `totale_documento(righe)` restituiscono lo stesso importo di prima.
- Chi vuole l'arrotondamento per documento deve passare esplicitamente
  `modalita_arrotondamento="per_documento"`.
- Un valore non ammesso solleva `ValueError`, sullo stile delle altre
  validazioni del modulo (aliquota sconosciuta, quantità negativa).
