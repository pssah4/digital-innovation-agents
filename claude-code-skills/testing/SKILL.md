---
name: testing
description: >
  Erstellt und verwaltet Unit Tests und Integration Tests. Analysiert die bestehende
  Codebase, erkennt das Test-Framework automatisch und generiert Tests die den
  Projekt-Konventionen folgen. Nutze diesen Skill wenn der User "Tests schreiben",
  "Unit Tests", "Integration Tests", "Test Coverage", "testen", "Tests fehlen",
  "Testabdeckung", "TDD" oder aehnliches erwaehnt. Auch nach einer Implementierung
  wenn Tests erstellt oder aktualisiert werden muessen.
disable-model-invocation: false
---

# Testing -- Unit & Integration Tests

Erstellt Tests die sich nahtlos in die bestehende Codebase einfuegen.
Erkennt Framework, Patterns und Konventionen automatisch aus dem Projekt.

## Codebase-Analyse zuerst

Bevor du einen einzigen Test schreibst, analysiere das Projekt:

```
1. Test-Framework erkennen:
   - package.json -> jest/vitest/mocha? (scripts.test, devDependencies)
   - pyproject.toml -> pytest? (tool.pytest)
   - Cargo.toml -> Rust built-in?
   - Bestehende Test-Dateien -> Welches Pattern?

2. Bestehende Test-Struktur erkennen:
   - Wo liegen Tests? (tests/, __tests__/, src/**/*.test.ts, *.spec.ts?)
   - Naming Convention? (.test.ts, .spec.ts, _test.py?)
   - Gibt es conftest.py / jest.config.ts / vitest.config.ts?
   - Gibt es Test-Utilities, Fixtures, Factories?

3. Bestehende Patterns uebernehmen:
   - Wie werden Mocks erstellt? (jest.mock, vi.mock, unittest.mock?)
   - Wie wird mit Async umgegangen?
   - Welche Assertions werden verwendet?
   - Gibt es Shared Test Helpers?

4. Was wird NICHT getestet? (Luecken identifizieren)
```

Wichtig: Folge IMMER den bestehenden Patterns. Fuehre keine neuen Test-Frameworks
oder -Patterns ein, es sei denn es gibt noch gar keine Tests.

## Testing-Pyramide

```
        /\
       /E2E\           Wenige, langsam, teuer
      /------\
     / Integr. \       Moderate Anzahl
    /------------\
   /  Unit Tests  \    Viele, schnell, guenstig
  /________________\
```

Fokus dieses Skills: **Unit Tests** und **Integration Tests**.
E2E-Tests sind ein separates Thema.

## Unit Tests

### Wann Unit Tests schreiben

- Fuer jede public Funktion/Methode mit Logik
- Fuer Utility-Funktionen und Helper
- Fuer Daten-Transformationen
- Fuer Fehlerbehandlung und Edge Cases
- NICHT fuer triviale Getter/Setter ohne Logik
- NICHT fuer reine Durchreich-Funktionen

### AAA Pattern (Arrange, Act, Assert)

Jeder Test folgt dem AAA Pattern:

```typescript
// Beispiel (TypeScript/Jest -- adaptiere ans Projekt-Framework)
describe('ToolRegistry', () => {
  describe('registerTool', () => {
    it('should register a tool and make it retrievable by name', () => {
      // Arrange
      const registry = new ToolRegistry();
      const tool = createMockTool({ name: 'read-file' });

      // Act
      registry.registerTool(tool);

      // Assert
      expect(registry.getTool('read-file')).toBe(tool);
    });

    it('should throw when registering duplicate tool names', () => {
      // Arrange
      const registry = new ToolRegistry();
      const tool = createMockTool({ name: 'read-file' });
      registry.registerTool(tool);

      // Act & Assert
      expect(() => registry.registerTool(tool))
        .toThrow(/already registered/);
    });
  });
});
```

### FIRST Prinzipien

- **Fast**: Tests muessen schnell laufen (<1s pro Test)
- **Independent**: Kein Test haengt von einem anderen ab
- **Repeatable**: Gleicher Input = gleicher Output, immer
- **Self-validating**: Pass oder Fail, kein manuelles Pruefen
- **Timely**: Tests direkt mit dem Feature schreiben

### Was testen -- Checkliste pro Funktion

Lies `references/test-checklist.md` fuer die vollstaendige Checkliste.

Kurzfassung:
- Happy Path (normaler Ablauf)
- Edge Cases (leere Eingaben, Grenzwerte, null/undefined)
- Error Cases (ungueltige Eingaben, fehlende Abhaengigkeiten)
- Boundary Conditions (min/max Werte, leere Arrays, grosse Daten)

### Mocking-Regeln

- Mocke **externe Abhaengigkeiten** (APIs, Dateisystem, Datenbank)
- Mocke NICHT die Einheit die du testest
- Bevorzuge Dependency Injection ueber globale Mocks
- Wenn das Projekt bereits Mock-Patterns hat, nutze diese

## Integration Tests

### Wann Integration Tests schreiben

- Wenn mehrere Module zusammenspielen
- Fuer API-Endpunkte (Request -> Response)
- Fuer Datenbankzugriffe (mit Test-DB oder In-Memory)
- Fuer Event/Message-Flows zwischen Komponenten

### Integration Test Regeln

- Reale Abhaengigkeiten wo moeglich, nur externe Services mocken
- Jeder Test ist unabhaengig (eigener State, eigenes Teardown)
- Realistische Testdaten, nicht "foo" / "bar" / "test"
- Timeouts fuer Async-Operationen setzen
- Setup/Teardown in beforeAll/afterAll fuer geteilte Ressourcen

### Datei-Benennung

Folge dem bestehenden Projekt-Pattern. Falls keines existiert:
- Unit Tests: `{module}.test.ts` oder `{module}.spec.ts`
- Integration Tests: `{module}.integration.test.ts`
- Im gleichen Verzeichnis wie der Source Code, oder in `tests/`

## Test-Workflow

### Fuer bestehendes Feature ohne Tests

```
/testing {Datei oder Modul}

1. Analysiere die Datei und ihre Abhaengigkeiten
2. Identifiziere testbare Funktionen/Methoden
3. Erkenne bestehende Test-Patterns im Projekt
4. Erstelle Tests (AAA Pattern, FIRST Prinzipien)
5. Fuehre Tests aus und verifiziere
6. Pruefe Coverage der neuen Tests
```

### Fuer neues Feature (nach /coding)

```
/testing

1. Lies die Feature-Spec (FEATURE-*.md) fuer Success Criteria
2. Identifiziere alle neuen/geaenderten Dateien
3. Erstelle Unit Tests fuer neue Module
4. Erstelle Integration Tests fuer Modul-Interaktionen
5. Verifiziere Success Criteria aus Feature-Spec
```

### Coverage-Ziele

| Metrik | Ziel | Minimum |
|--------|------|---------|
| Line Coverage | 85% | 70% |
| Branch Coverage | 80% | 65% |
| Function Coverage | 90% | 75% |

Diese sind Richtwerte. Projekt-spezifische Ziele aus CLAUDE.md oder
Feature-Specs haben Vorrang.

## Anti-Patterns vermeiden

Lies `references/test-anti-patterns.md` fuer Details.

Kurzfassung:
- **Kein Testing von Implementierungs-Details**: Teste Verhalten, nicht interne Mechanik
- **Kein uebertriebenes Mocking**: Wenn du 5+ Mocks brauchst, hat der Code ein Design-Problem
- **Keine trivialen Tests**: `expect(1+1).toBe(2)` hilft niemandem
- **Keine fragilen Tests**: Tests die bei jedem Refactoring brechen testen falsch
- **Keine Tests die setTimeout/setInterval pruefen**: Teste das Ergebnis, nicht den Timer

## Codebase-Awareness

Vor dem Schreiben von Tests IMMER:
- Bestehende Test-Dateien lesen und Patterns uebernehmen
- Test-Utilities und Shared Fixtures wiederverwenden
- Sich an bestehende Naming Conventions halten
- Projekt-spezifische Test-Konfiguration respektieren (jest.config, vitest.config, etc.)

## Keywords
Tests, Unit Tests, Integration Tests, Test Coverage, testen, TDD,
Testabdeckung, Testing, Testfaelle, Testpyramide
