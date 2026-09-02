# listino — repo di prova per la fucina

Progetto minuscolo ma realistico, creato per collaudare il loop dell'agente sviluppatore.
Non serve ad altro: se lo rompi non succede niente, ed è il punto.

Calcola importi di listino: sconti percentuali, IVA, totali di riga e di documento.
Tutti gli importi sono `Decimal`, mai `float`.

## Uso

    pip install -e ".[dev]"
    pytest -q

19 test, tutti verdi. La CI li esegue su ogni push e su ogni PR.

## Lavori non ancora fatti

Sono i candidati per le prime issue da dare all'agente, in ordine di difficoltà
crescente.

1. **Sconto a valore fisso.** Oggi `applica_sconto` accetta solo una percentuale.
   Serve poter scontare di 5,00 € invece che del 10%.
2. **Esenzione IVA.** Serve un'aliquota a zero con causale obbligatoria (art. 15,
   fuori campo, non imponibile), perché in fattura la causale va stampata.
3. **Arrotondamento per riga o per documento.** Oggi si arrotonda riga per riga e poi
   si somma. Su documenti lunghi questo produce uno scostamento di qualche centesimo
   rispetto all'arrotondamento del solo totale. Va reso configurabile.
   *Quale dei due deve essere il default non è deciso.*
