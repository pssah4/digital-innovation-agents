# Test-Checkliste pro Funktion/Methode

## Happy Path

- Normaler Aufruf mit gueltigem Input -> erwartetes Ergebnis
- Verschiedene gueltige Input-Varianten (wenn applicable)

## Edge Cases

- Leerer Input (leerer String, leeres Array, leeres Objekt)
- null / undefined / None als Input
- Grenzwerte (0, -1, MAX_INT, leeres Array mit length 0)
- Einzelnes Element (Array mit 1 Item, String mit 1 Char)
- Unicode / Sonderzeichen in Strings
- Sehr grosse Eingaben (Performance-Relevanz)

## Error Cases

- Ungueltiger Input-Typ (String statt Number, etc.)
- Fehlende Pflichtfelder
- Ungueltige Werte (negative Zahlen wo positiv erwartet, etc.)
- Fehlende/nicht erreichbare Abhaengigkeiten
- Timeout-Szenarien (fuer Async-Operationen)
- Korrekte Error Messages und Error Codes

## State-Abhaengige Tests

- Initiale State (vor erstem Aufruf)
- Nach Mutation (nach Hinzufuegen, Aendern, Loeschen)
- Concurrent Access (wenn relevant)
- Idempotenz (gleicher Aufruf, gleiches Ergebnis)

## Integration-spezifisch

- Korrekte Weiterleitung zwischen Modulen
- Daten-Transformation an Modul-Grenzen
- Error Propagation durch die Kette
- Korrekte Reihenfolge von Operationen

## Coverage-Strategie

Nicht jede Funktion braucht alle Checks. Priorisiere:

1. **Kritischer Pfad**: Immer vollstaendig testen
2. **Fehlerbehandlung**: Immer testen (oft die wichtigsten Tests)
3. **Edge Cases**: Fuer Funktionen mit komplexer Logik
4. **Triviale Getter/Setter**: Nicht testen (ausser sie haben Logik)
