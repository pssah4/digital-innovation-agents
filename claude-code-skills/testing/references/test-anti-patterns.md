# Test Anti-Patterns

## 1. Implementierungs-Details testen

```
FALSCH: Teste dass intern Array.sort() aufgerufen wird
RICHTIG: Teste dass das Ergebnis sortiert ist

FALSCH: Teste dass eine private Methode aufgerufen wird
RICHTIG: Teste das oeffentliche Verhalten das daraus resultiert
```

Warum: Tests an Implementierung gekoppelt brechen bei jedem Refactoring.

## 2. Uebertriebenes Mocking

```
FALSCH: 5+ Mocks fuer einen einzigen Test
RICHTIG: Maximal 2-3 Mocks, rest ueber Dependency Injection

FALSCH: Mock der Einheit die du testest
RICHTIG: Nur externe Abhaengigkeiten mocken
```

Warum: Zu viele Mocks testen den Mock-Code, nicht die Logik.
Wenn ein Test viele Mocks braucht, hat der Code ein Design-Problem.

## 3. Triviale Tests

```
FALSCH:
  it('should return true', () => {
    expect(true).toBe(true);
  });

FALSCH:
  it('should set name', () => {
    user.name = 'Max';
    expect(user.name).toBe('Max');
  });

RICHTIG: Teste nur Logik die schiefgehen kann
```

## 4. Fragile Tests

```
FALSCH: Teste exakte Fehlermeldung als String
  expect(error.message).toBe('User with ID 42 not found in database schema "public"');

RICHTIG: Teste auf relevanten Teil
  expect(error.message).toContain('not found');
  expect(error.code).toBe('USER_NOT_FOUND');
```

## 5. Test-Abhaengigkeiten

```
FALSCH: Test B braucht Ergebnis von Test A
RICHTIG: Jeder Test hat eigenes Setup und ist unabhaengig ausfuehrbar
```

## 6. Nicht-deterministische Tests

```
FALSCH: Teste mit Date.now() oder Math.random()
RICHTIG: Injiziere Zeitquelle und Zufallsgenerator, oder fixiere Werte
```

## 7. God-Tests

```
FALSCH: Ein Test der 20 Assertions hat
RICHTIG: Ein Test, ein Verhalten, wenige verwandte Assertions
```

## 8. Copy-Paste Tests ohne Variation

```
FALSCH: 10 Tests die sich nur im Input unterscheiden
RICHTIG: Parametrisierte Tests (test.each / @pytest.mark.parametrize)
```

## 9. Tests die nur Coverage treiben

```
FALSCH: Test der eine Funktion aufruft aber nichts assertiert
RICHTIG: Jeder Test hat mindestens eine sinnvolle Assertion
```

## 10. Sleep/Delay in Tests

```
FALSCH: await sleep(1000); expect(result).toBe(true);
RICHTIG: Nutze waitFor, polling, oder Events statt feste Wartezeiten
```
