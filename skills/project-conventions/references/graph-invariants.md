# V-Model-Artefakt-Graph - Invarianten

Single Source of Truth fuer die Konsistenz-Invarianten, die der Skill
`/consistency-check` und alle anderen V-Model-Skills einhalten. Jede
Invariante hat eine ID (`N-n` fuer Node-Invarianten, `E-n` fuer Edge-
Invarianten, `S-n` fuer semantische Invarianten), einen Text und eine
Pruefregel.

Wenn ein V-Model-Skill diese Datei aktualisiert, muss `/consistency-check`
Mode A entsprechend angepasst werden.

## Graph-Modell

**Knoten (Artefakt-Typen):**

- `Project-BA` - `_devprocess/analysis/BA-{PROJECT}.md` (Singleton, Produkt-Schicht; Personas, Value, Nordstern)
- `Item-BA` - eine BA-Datei pro neuem Backlog-Item, flach in `_devprocess/analysis/`:
   - `BA-EPIC-{nn}-{slug}.md` (Pflicht vor neuem Epic)
   - `BA-FEAT-{ee}-{ff}-{slug}.md` (Pflicht vor neuem Feature)
   - `BA-IMP-{ee}-{ff}-{nn}-{slug}.md` (optional)
   - `BA-FIX-{ee}-{ff}-{nn}-{slug}.md` (optional)
- `BA-Section` - eine Ueberschrift in `Project-BA` oder einem `Item-BA`
 (Personas, JTBDs, Problem, Value Props, KPIs, Risks, usw.)
- `Epic` - `docs/requirements/epics/EPIC-{nn}-{slug}.md`
- `Feature` - `docs/requirements/features/FEATURE-*.md`
- `SC` - eine Zeile in der Success-Criteria-Tabelle eines Features
- `ADR` - `docs/adr/ADR-{nn}-{slug}.md`
- `arc42-Section` - eine Ueberschrift in
 `docs/architecture/arc42.md` (§1..§12)
- `PLAN` - `docs/implementation/plans/PLAN-{nn}-{slug}.md`
- `FIX` - `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` (Bug-/Issue-Followup, Pflicht-Bindung an Feature/Epic)
- `IMP` - `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md` (technische Verbesserung, Pflicht-Bindung an Feature/Epic)
- `Code` - eine Datei oder Zeilenspanne unter `src/`

> **Hinweis (2026-04-21):** Die alten Konzepte `BL-Item (historisch)` und
> `Chore` wurden abgeschafft. Bugs/Issues werden als **FIX**, technische
> Aenderungen ohne Feature-Charakter als **IMPROVEMENT** (kurz **IMP**)
> gefuehrt. Beide haben verpflichtend ein `feature:` und `epic:` im
> Frontmatter, weil jeder Code aus einem Feature-Kontext entsteht.

**Kanten (Referenz-Typen):**

- `Item-BA -> Project-BA` (Item-BA Frontmatter `project-ba-ref` zeigt auf Project-BA)
- `Project-BA.Persona -> Item-BA` (Item-BA referenziert Persona-ID via `personas:` im Frontmatter)
- `Item-BA -> Epic|Feat|Imp|Fix` (Promotion: das Backlog-Item traegt `ba-ref:` auf die Item-BA-Datei)
- `Item-BA.KPI -> Project-BA.KPI` (einzahlend: Frontmatter `project-kpi-ref`)
- `BA.Persona -> Epic` (Zugehoerigkeit: welches Epic adressiert welche Persona)
- `BA.JTBD -> Feature` (adressiert: welcher JTBD wird durch welches Feature geloest)
- `Epic -> Feature` (enthaelt: MVP-Features-Tabelle im Epic)
- `Feature -> SC` (hat: Success-Criteria-Tabelle im Feature)
- `Feature -> ADR` (referenziert: Related-ADRs-Abschnitt im Feature)
- `Feature -> Code` (implementiert: Source-Pfade im Feature)
- `ADR -> arc42-Section` (belegt: arc42 §9 Tabelle)
- `ADR -> ADR` (supersedes / related)
- `PLAN -> Feature` (realisiert: feature-refs im PLAN-Frontmatter)
- `PLAN -> ADR` (realisiert: adr-refs im PLAN-Frontmatter)
- `FIX -> Feature` / `FIX -> Epic` (Pflicht: gehoert zu)
- `IMP -> Feature` / `IMP -> Epic` (Pflicht: gehoert zu)
- `* -> *` **depends-on** (Implementierungs-Reihenfolge; Artefakt wartet
 auf die Fertigstellung eines anderen; gerichtet, azyklisch)

## Node-Invarianten

| ID | Invariante | Pruefregel |
| ---- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| N-1 | Jedes Feature hat genau einen Epic-Parent. | Feature-Frontmatter oder -Header enthaelt `Epic:` Link zu existierendem Epic. |
| N-2 | Jedes Epic hat mindestens ein Feature in MVP-Tabelle oder ist `Phase: Candidates`. | Epic-Datei `## MVP Features` Tabelle ist nicht leer, oder Phase-Candidates-Marker vorhanden. |
| N-3 | Jede ADR ist mindestens einmal referenziert (Feature, arc42 oder Backlog). | Grep nach ADR-ID in allen Features, arc42, Backlog. |
| N-4 | Jedes Feature hat mindestens einen Success-Criterion-Eintrag (Platzhalter erlaubt). | Feature `## Success Criteria`-Tabelle hat mind. eine Zeile, auch `[AWAITING BA]` ist gueltig. |
| N-5 | Jedes Feature mit `status: Implemented` hat einen `## Codebase-Verifikation` Abschnitt. | Section-Header existiert. |
| N-6 | Jedes FIX/IMP hat ein Phase-Label (`Released | Building | Planned | Candidates`). | Spalte oder Notizen-Prefix `[Phase: ...]` vorhanden. |
| N-7 | Jedes FIX/IMP mit `Phase: Candidates` hat `needs refinement: {Grund}`-Marker. | Notizen-Feld enthaelt den Marker. |
| N-8 | Jedes Item-BA (`BA-EPIC-*`, `BA-FEAT-*`, `BA-IMP-*`, `BA-FIX-*`) hat ein `project-ba-ref:` im Frontmatter (Wert zeigt auf existierenden Project-BA, oder `null` wenn kein Project-BA existiert) und definiert keine Personas/Value-Dimensionen/Nordstern lokal, wenn `project-ba-ref` gesetzt ist. | Frontmatter parsen, `project-ba-ref` auf existenz pruefen; bei gesetztem Wert: Item-BA enthaelt keine eigene Persona-Definition (Persona wird per ID aus Project-BA §2 referenziert). |
| N-9 | Jedes EPIC und FEAT, das eine zugehoerige BA-Datei in `analysis/` hat, traegt `ba-ref:` im Frontmatter, das auf diese Datei zeigt. Umgekehrt zeigt jeder Item-BA-Filename auf ein passendes Backlog-Item (BA-EPIC-04 -> EPIC-04). | Frontmatter `ba-ref:` parsen, Pfad pruefen; Filename-zu-ID-Mapping ueber Naming-Pattern verifizieren. |
| N-10 | Feature-Frontmatter traegt KEINEN Lifecycle-`status:`- und KEINEN `phase:`-Wert. Beide Felder leben in der Backlog-Row (Single-Source-of-Truth, siehe `project-conventions/SKILL.md`). Ausnahme fuer Reverse-Engineered Artefakte: ein einmaliges `status: Observed (not validated)` darf im Frontmatter stehen, bis `/business-analysis` das Feature validiert; danach wird das Feld entfernt. | YAML-Frontmatter parsen, `phase:` auf Abwesenheit pruefen; `status:` nur tolerieren, wenn der Wert ein Reverse-Engineered-Marker ist (`Observed`, `Inferred`, `Draft (reverse-engineered, ...)`); sonst `frontmatter-status-leak`. |
| N-11 | Epic-Frontmatter traegt KEINEN Lifecycle-`status:`- und KEINEN `phase:`-Wert. Ausnahme: Reverse-Engineered Epics duerfen `status: Anticipated (not yet validated)` tragen, bis `/business-analysis` und `/requirements-engineering` sie verfeinern. | YAML-Frontmatter parsen, `phase:` ablehnen; `status:` nur als Reverse-Engineered-Marker tolerieren. |
| N-12 | Jedes ADR-Frontmatter enthaelt `status: Proposed|Accepted|Superseded|Deprecated` (ADR-eigenes Statusfeld, MADR-Konvention; nicht zu verwechseln mit dem Backlog-Status der ADR-Row). Kein `phase:` im ADR-Frontmatter. | YAML-Frontmatter parsen, ADR-Status-Wert pruefen. |
| N-13 | Jede FIX-Datei hat `feature:` (Pflicht) und `epic:` (Pflicht) im Frontmatter. Beide Felder zeigen auf existierende Artefakte. | YAML-Frontmatter parsen; FIX-Felder vs docs/requirements. |
| N-14 | Jede IMP-Datei (IMPROVEMENT) hat `feature:` (Pflicht) und `epic:` (Pflicht) im Frontmatter. Beide zeigen auf existierende Artefakte. | YAML-Frontmatter parsen; IMP-Felder vs docs/requirements. |
| N-15 | FIX- und IMP-Dateien tragen wie Features KEINEN `status:`- und KEINEN `phase:`-Wert im Frontmatter. State lebt in der Backlog-Row. | YAML-Frontmatter parsen. |
| N-16 | Die alten Begriffe "Chore" und "BL-Item (historisch)" sowie der Backlog-Abschnitt `## Standalone Chores` werden nicht mehr verwendet. | Grep auf "Chore"/"BL-Item (historisch)"/"Standalone Chores" in docs/ (archive ausgenommen). |
| N-17 | Status-Kohaerenz zwischen Eltern- und Kind-Artefakten: ein Eltern-Artefakt darf nicht in einem Pre-Validation-Status verharren, wenn ein abgeleitetes Kind-Artefakt nachweislich exerzitiert wurde. Pruefpaare siehe Tabelle "Status-Coherence-Pairs" unten. | Pro Paar: Eltern-Frontmatter `status:` lesen, Kind-Evidenz pruefen (Datei-Existenz oder Kind-Phase >= Building); bei Treffer Finding `status-coherence-breach`. |
| N-18 | Jedes FEATURE mit Backlog-Status `Done` enthaelt eine nicht-leere `## Activation Path` Section in der Definition of Done (Pflicht-Felder Type und Identifier ausgefuellt). FEATUREs ohne `subtype:` im Frontmatter sind aus Rueckwaerts-Kompatibilitaet ausgenommen; FEATUREs mit `subtype: user-facing` (Default wenn gesetzt) oder `subtype: library` muessen die Invariante erfuellen. | Pro Done-FEATURE: `## Activation Path` Section parsen, Type und Identifier extrahieren, beide muessen nicht-leer sein. Severity warn (fail unter --strict). |
| N-19 | Jede Artefakt-ID (FEAT, FIX, IMP, ADR, PLAN) erscheint hoechstens einmal als Tabellenzeile in `_devprocess/context/BACKLOG.md`. EPIC ist ausgenommen, weil Epic-IDs absichtlich sowohl als Header (`### EPIC-NN: ...`) als auch als Tabellenzeile vorkommen. | Backlog-Datei zeilenweise scannen, Tabellenzeilen mit `^\|\s*(FEAT|FIX|IMP|ADR|PLAN)-...` sammeln, Anzahl pro ID pruefen. Severity high (Downstream-Tools wie Issue-Lookup koennen Duplikate nicht aufloesen). |

## Edge-Invarianten

| ID | Invariante | Pruefregel |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| E-1 | Jeder Markdown-Link auf projekt-interne Pfade ist gueltig. | Regex auf `](docs/...)`, `](../...)`, `](src/...)`, Pfad-Existenz-Check. |
| E-2 | Jeder `Source (Implementation)`-Pfad im Feature existiert oder Phase in {Planned, Candidates}. | Feature-Source-Pfade vs. Dateisystem. |
| E-3 | Jede ADR in Feature `Related-ADRs` existiert unter `docs/adr/`. | ADR-IDs vs. `docs/adr/`-Inhalt. |
| E-4 | Jede ADR in arc42 §9 Tabelle existiert unter `docs/adr/`. | arc42 §9 Zeilen vs. `docs/adr/`-Inhalt. |
| E-5 | Jede ADR unter `docs/adr/` ist in arc42 §9 Tabelle ODER als deprecated markiert. | `docs/adr/`-Inhalt vs. arc42 §9. |
| E-6 | Jede FIX/IMP-Zeile mit Feature/ADR/PLAN-Spalte zeigt auf existierendes Artefakt. | Link-Check pro Zeile. |
| E-7 | Backlog-Feature-Zeile `Phase` stimmt mit der Phase-Spalte des Epic-Headers ueberein, in dessen Section die FEAT-Row liegt. Die Phase eines FEAT entspricht der Phase seines Epic. | Fuer jede FEAT-Row: gefundene Phase-Spalte vs. Phase im Epic-Header darueber. (Frueher: Vergleich gegen Frontmatter-Phase, abgeschafft mit N-10/N-11.) |
| E-8 | Backlog-Epic-Header `Phase: ...` ist konsistent: alle FEAT-Rows unter dem Epic tragen dieselbe Phase wie der Header (worst-wins-Ableitung). | Fuer jeden Epic-Header: Phase aus dem Header lesen, alle FEAT-Rows darunter pruefen. |
| E-9 | Dashboard-Counts im Backlog stimmen mit Summe der Status- und Phase-Spalten der Backlog-Rows ueberein. | Dashboard-Tabelle neu berechnen, indem alle Backlog-Rows (FEAT, IMP, FIX) gezaehlt werden, gruppiert nach Status- und Phase-Spalten-Wert. (Frueher: Berechnung aus Frontmatters, abgeschafft mit N-10/N-11.) |
| E-10 | `depends-on`-Referenzen in Feature/Epic/ADR/FIX/IMP-Frontmatter zeigen auf existierende Artefakte. | YAML-Feld parsen, Ziel-ID im Dateisystem pruefen. |
| E-11 | Der `depends-on`-Graph ist azyklisch (DAG). Keine Implementierungs-Zyklen. | Topologisches Sortieren ueber alle `depends-on`-Kanten; Zyklen detektieren. |
| E-14 | Bidirektionale Bindung zwischen `FIXME(stub):` Markern im Source-Code und FIX-Rows im Backlog. Jeder Marker referenziert eine offene FIX-ID; jede FIX-Row die einen Stub dokumentiert (Notes enthalten `Wiring offen`, `stub`, oder `deferred-stub`) referenziert mindestens eine Source-Stelle. | Grep auf `FIXME(stub):` im Source-Tree (Pattern fuer `//` und `#` Comment-Style), FIX-ID extrahieren, gegen Backlog cross-checken. Umgekehrt: FIX-Row-Notes scannen, FIX-ID gegen Source-Tree gruepen. |

> Anmerkung: E-12 und E-13 werden in `skills/consistency-check/SKILL.md`
> bereits genutzt (Backlog-Completeness und ARCHITECTURE.map-Entrypoints).
> Diese Datei fuehrt sie aktuell noch nicht. Konsolidierung in einem
> separaten Pflege-Pass.

## Semantische Invarianten (Mode B, nur on-demand)

| ID | Invariante | Pruefregel |
| --- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| S-1 | Feature-Beschreibung widerspricht nicht den referenzierten ADRs. | Subagent liest Feature + alle Related ADRs, meldet inhaltliche Widersprueche. |
| S-2 | Feature ohne passendes BA-JTBD ist explizit geflaggt. | Subagent prueft: hat das Feature einen JTBD-Verweis in BA? Wenn nein, FIX/IMP `needs BA-anchor`. |
| S-3 | arc42-Sektion zur ADR-Decision spiegelt aktuellen ADR-Text, nicht eine alte Revision. | Subagent liest arc42-Sektion + zitierte ADR, meldet Drift. |
| S-4 | Features mit `status: Implemented` haben ihre SCs plausibel im Code belegbar. | Subagent stichprobenartig pro Feature; Ergebnis im Codebase-Verifikations-Abschnitt. |
| S-6 | Jedes FEATURE mit Backlog-Status `Done` mappt jede Success-Criterion-Zeile auf einen konkreten Code-Pfad (file:line oder Symbol). | Subagent liest FEATURE und das Code-Pfad-Verzeichnis (ARCHITECTURE.map als Index), berichtet `sc-without-evidence` fuer SCs ohne klaren Code-Bezug. |
| S-7 | Der `## Activation Path` Eintrag eines Done-FEATURE existiert tatsaechlich im Code. | Subagent prueft pro Aktivierungstyp (route, command, public-API, ...) ob der angegebene Identifier im Source-Tree vorkommt; berichtet `activation-path-missing` falls nicht. |

## Status-Coherence-Pairs (Pruefpaare fuer N-17)

N-17 vergleicht den Status eines Eltern-Artefakts mit der Phase oder
Existenz seines abgeleiteten Kind-Artefakts. Wenn das Kind nachweislich
exerzitiert wurde (Datei existiert oder Phase ist `Building` oder
`Released`), darf das Eltern-Artefakt nicht mehr in einem Pre-
Validation-Status verharren.

| Eltern-Typ | Eltern-Status (Pre-Validation) | Kind-Evidenz (Trigger fuer Breach) |
| ---------- | ------------------------------ | ---------------------------------- |
| BA | `Draft` oder `Draft (...)`-Praefix (z. B. `Draft (reverse-engineered, ...)`) | `_devprocess/requirements/handoff/architect-handoff.md` existiert UND referenziert diese BA, ODER ein Epic / Feature / IMP / FIX mit `ba-ref:` auf diese BA hat Phase `Building` oder `Released`. |
| ADR | `Proposed` | Ein Feature mit `adr-refs:` (oder `Related-ADRs:`) auf diese ADR hat Phase `Building` oder `Released`. |

Erweiterungen der Tabelle erfolgen nur, wenn ein neues Eltern-Kind-
Verhaeltnis im V-Modell etabliert wird (z. B. PLAN als Eltern-
Artefakt). Tabelle ist append-only; bestehende Zeilen aendern sich nur
mit explizitem Versionierungshinweis.

**Match-Regel fuer Eltern-Status:**

- `Draft (...)` matcht den Praefix `Draft` mit beliebigem Klammer-
 Inhalt (z. B. `Draft (reverse-engineered, 2026-04-12)`). Zweck:
 BAs aus `/reverse-engineering` werden gleich behandelt wie roh
 angelegte Drafts.
- `Validated`, `Confirmed by usage`, `Accepted`, `Superseded`,
 `Deprecated` zaehlen NICHT als Pre-Validation und triggern N-17
 nicht.

**Severity:** N-17 ist standardmaessig `warn`. Unter `--strict`
(z. B. vor Release) wird `warn` zu `fail`. Status-Inkohaerenz ist ein
Qualitaetshinweis, keine strukturelle Beschaedigung des Graphen.

**Auto-Fix:** Nicht automatisch. Status-Promotion ist eine semantische
Aussage und gehoert in den jeweiligen Phase-Skill (BA -> `/business-analysis`,
RE -> `/requirements-engineering` ueber den Handoff-Promotion-Pfad,
Architecture -> `/architecture` fuer ADR-Status). Mode A meldet das
Finding; Mode C bietet "Open phase skill" als Fix-Option an.

## FEATURE-Subtyp und Activation-Path (fuer N-18 und S-6 / S-7)

Jedes FEATURE traegt einen Subtyp im Frontmatter, der den Aktivierungs-
Vertrag bestimmt. Subtyp-Default beim Anlegen: `user-facing`.

| Subtyp | Frontmatter | Wann nutzen | Aktivierungs-Pflicht |
|--------|-------------|-------------|----------------------|
| `user-facing` | `subtype: user-facing` | UI, CLI-Command, API-Endpunkt, Scheduled-Job, Plugin-Command, Hotkey, Agent-Tool, Web-Route, Mobile-Screen | Mindestens ein dokumentierter Trigger im `## Activation Path` Block der FEATURE-Spec; Trigger muss im Code existieren. |
| `library` | `subtype: library` | Public API ohne End-User-Trigger (Funktion, Klasse, Modul, Package-Export) | Public Symbol(e) im `## Activation Path` Block; Symbol(e) muessen exportiert sein und in API-Doku auftauchen. |

**Rueckwaerts-Kompatibilitaet:** FEATUREs ohne `subtype:` im Frontmatter
sind aus N-18, S-6, S-7 ausgenommen. Neue FEATUREs schreiben `subtype:`
verbindlich. Existierende Projekte koennen den Subtyp pro FEATURE
nachpflegen, ohne dass eine harte Migration noetig ist.

**`## Activation Path` Format in der FEATURE-Spec:**

```markdown
## Activation Path

- Type: command | route | UI-element | endpoint | scheduled-job | tool | hotkey | public-API
- Identifier: `<Identifier>`
- Where it lives: <Datei oder ARCHITECTURE.map-Konzept>
- How a user (or caller) reaches it: <ein Satz>
```

`Type` und `Identifier` sind Pflicht und nicht-leer. Mode A pruefst
das ueber N-18; Mode B prueft via S-7 ob der Identifier im Code
tatsaechlich vorkommt.

## FIXME(stub)-Marker-Konvention (fuer E-14)

Stub-Implementierungen (no-op Hooks, Hard-Coded-Placeholder, leere
Returns die spaeter durch echte Logik ersetzt werden sollen) MUESSEN
einen `FIXME(stub):`-Marker im Source-Code tragen UND eine paarige
FIX-Row im Backlog haben. Bidirektionale Bindung; Mode A prueft beide
Richtungen ueber E-14.

**Marker-Syntax (Comment-Style je Sprache):**

```
// FIXME(stub): <Grund in einem Satz> -- see FIX-{ee}-{ff}-{nn}
# FIXME(stub): <Grund in einem Satz> -- see FIX-{ee}-{ff}-{nn}
```

Verwendung:

- `//` fuer C-Familie: TypeScript, JavaScript, Java, Go, Rust, C#,
 Swift, Kotlin, React (TSX/JSX).
- `#` fuer Python, Ruby, R, Shell-Skripte.

Andere Comment-Stile (`--` SQL, `;` Lisp, `<!-- -->` HTML/XML) werden
aktuell nicht von Mode A erkannt; bei Bedarf ueber dia.config.json
erweitern.

**Pflicht-Inhalt der zugehoerigen FIX-Row** im Backlog und in der
Detail-Datei `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`:

- Status `Open` oder `Active` (nicht `Done`, sonst Marker-Drift).
- Notes-Feld enthaelt mindestens `Wiring offen`, `stub`, oder
 `deferred-stub`, damit Mode A den Stub-Charakter erkennt.
- Mindestens eine Datei-Referenz auf eine Source-Stelle, die den
 Marker traegt.

**Aufloesungs-Regel:** Wenn der Stub durch echte Implementierung
ersetzt wird, MUESSEN beide Seiten mit demselben Commit aufgeraeumt
werden: Marker entfernen, FIX-Row auf `Done` setzen, Detail-Datei
mit Aufloesungs-Notiz im `## Fix` Abschnitt versehen. Mode A flaggt
sonst entweder `stub-without-fix-row` (Marker bleibt nach FIX Done)
oder `fix-without-stub-evidence` (FIX bleibt Open nachdem Marker
entfernt wurde).

## Phase/Status-Frontmatter-Konvention (verbindlich fuer alle Skills)

**Pflichtfelder im YAML-Frontmatter:**

| Artefakt | Pflichtfelder | Default beim Anlegen |
| -------- | ----------------------------------------------------------------------- | ------------------------------- |
| Project-BA | `type: ba`, `target-type: project`, `target-id: {PROJECT}`, `created:` | `type: ba`, `target-type: project` |
| Item-BA | `type: ba`, `target-type: epic|feat|imp|fix`, `target-id:`, `project-ba-ref:` (Pfad oder `null`), `personas:` (IDs), `project-kpi-ref:` (Liste), `created:` | `target-type` aus Triage; `personas: []` falls noch keine Refs |
| Epic | `ba-ref:` (Pflicht ab N-9). KEIN `phase:`, KEIN `status:` im Frontmatter; beide leben in der Backlog-Row. | Frontmatter ohne Status/Phase |
| Feature | `subtype: user-facing|library` (optional fuer Bestand, Pflicht fuer neue FEATUREs ab N-18); `ba-ref:` (Pflicht ab N-9). KEIN `status:`, KEIN `phase:` im Frontmatter. | `subtype: user-facing`, BACKLOG-Row mit `status: Ready, phase: Building` |
| ADR | `status: Proposed|Accepted|Superseded|Deprecated` (ADR-Frontmatter, MADR). KEIN `phase:`. | Frontmatter `status: Proposed`, BACKLOG-Row mit `status: In Progress, phase: Building` |
| PLAN | `status: Draft|Active|Completed` (PLAN-Frontmatter). | Frontmatter `status: Draft`, BACKLOG-Row mit `status: In Progress, phase: Building` |
| FIX/IMP | `feature:` (Pflicht), `epic:` (Pflicht), `ba-ref:` falls eine BA existiert (sonst weglassen). KEIN `status:`, KEIN `phase:` im Frontmatter. | BACKLOG-Row mit `status: Ready, phase: Building` |

**Backlog-Status-Werte (Enum):** `Backlog | Ready | In Progress |
In Review | Done`. Diese Werte stehen in der `Status`-Spalte der
Backlog-Row und werden 1:1 mit der GitHub-Project-Status-Spalte
synchronisiert (`flow.py sync-status`). Sie sind **nicht** mit den
ADR/PLAN-Frontmatter-Status-Werten zu verwechseln, die parallel in
den jeweiligen Artefakten leben.

**Phase-Werte (Enum):** `Released | Building | Planned | Candidates`.
Phase steht in der Backlog-Row und beschreibt die Epic-Lebenszyklus-
Stufe. Siehe Phase-Schema-Konvention unten fuer Semantik.

**Frontmatter-Status (per Artefakt-Typ, lebt NUR im Frontmatter, nicht im Backlog):**

- ADR-Status (MADR): `Proposed | Accepted | Superseded | Deprecated`
- PLAN-Status: `Draft | Active | Completed`
- Feature, Epic, FIX, IMP: kein Frontmatter-Status. State steht
  ausschliesslich in der Backlog-Row.

**Single Source of Truth:** Die Backlog-Row ist die Wahrheit fuer
Status und Phase eines Artefakts. ADR- und PLAN-Frontmatter-Status
sind separate, artefaktspezifische Lifecycle-Felder, die nicht im
Backlog auftauchen.

**Sync-Pflicht bei State-Aenderungen:**

1. Backlog-Row aktualisieren (Status, Phase, Last-Change, Claim).
   Das ist der Schritt, der die Wahrheit setzt.
2. Bei ADR/PLAN: zusaetzlich das Frontmatter-Status-Feld in der
   Datei selbst pflegen (fuer Lifecycle-Zwecke, nicht fuer
   Backlog-Synchronisation).
3. Wenn Epic-Phase neu abgeleitet werden muss (worst-wins ueber
 Features): Epic-Frontmatter und Epic-Header-Zeile im Backlog
 aktualisieren.
4. Dashboard-Counts im Backlog (Phase-Tabelle) neu berechnen.
5. Epic-KPI-Referenzen (falls betroffen) pruefen.

Diese Sync-Kette wird in Skills `requirements-engineering`,
`architecture`, `coding`, `reverse-engineering` ohne Rueckfrage
ausgefuehrt. `/consistency-check` pruft sie ueber N-10, N-11, N-12,
E-7, E-8, E-9.

**Worst-Wins fuer Epic-Phase:**

`Released < Building < Planned < Candidates` (niedriger = weiter
fortgeschritten). Epic-Phase = maximales Rank-Level der enthaltenen
Features. Ein einziges Building-Feature macht das Epic Building.
Details siehe "Ableitung" im Phase-Schema-Abschnitt.

---

## Phase-Schema-Konvention (2026-04-20, aktualisiert)

Jedes Feature traegt eine **Phase**. Features sind die primaere
Quelle der Phase-Zuordnung. Epics/ADRs/PLANs/FIX/IMPs erben ihre
Phase vom Feature-Graph (Details siehe "Ableitung" unten).

- `Released` - vollstaendig implementiert, ausgeliefert und gegen
 Codebase verifiziert. Alle SCs im Code belegt UND alle
 referenzierten ADRs ebenfalls Released.
- `Building` - in aktiver Umsetzung oder umsetzungsreif; Scope, AK
 und Abhaengigkeiten geklaert.
- `Planned` - vorgesehen, noch nicht gestartet. Refinement
 weitgehend vorhanden.
- `Candidates` - Ideen und Optionen ohne verbindliche Zusage.
 Refinement ausstehend. `needs refinement: {Grund}` Pflicht.
 Moegliche Gruende: `Analyse fehlt`, `Zielgruppe unklar`,
 `Scope offen`, `Architektur offen`, `Baseline-Messung fehlt`.

**Ableitung:**

- **Feature-Phase**: aus `Codebase-Verifikation` (direkte Angabe).
 Downgrade: wenn ein referenzierter ADR nicht Released ist, ist das
 Feature maximal Building, nicht Released.
- **Epic-Phase**: worst-wins ueber alle enthaltenen Features (ein
 Building unter den Features -> Epic Building).
- **ADR-Phase**: Phase des Features, das auf es zeigt; bei mehreren
 Owner-Features worst-wins. Orphan-ADRs fallen in Candidates.
- **PLAN-Phase**: Phase des Features, das der PLAN realisiert.
- **FIX/IMP-Phase**: Phase des Features (oder ADRs), das das FIX/IMP
 referenziert.

**Legacy-Mapping** (fuer Projekte mit alten Phase-Labels, automatisch
durch `/consistency-check` und den Graph-Viewer gemappt):

- `Fertig` -> `Released`
- `Umsetzung` -> `Building`
- `Roadmap` -> `Planned`
- Neu: `Candidates` (frueher implizit in Roadmap enthalten).

## Wie Skills mit diesen Invarianten umgehen

- `/reverse-engineering` Phase 8: ruft `/consistency-check` im Mode A
 auf, behandelt gefundene Luecken als Phase-8-Output.
- `/requirements-engineering`: erzeugt Features so, dass N-1, N-4
 eingehalten werden. Verweist auf Epic-ID und legt SCs an (mind. als
 Platzhalter).
- `/architecture`: erzeugt ADRs so, dass N-3, E-5 nicht verletzt
 werden (arc42 §9 Tabelle wird aktualisiert beim Anlegen einer neuen
 ADR).
- `/coding`: fuehrt Mid-Course Feature-Capture-Dialog wenn neue
 user-facing Capabilities hinzukommen (N-1, N-4, BA-Anker).
- `/dia-guide`: ruft `/consistency-check` beim Start (Mode A)
 und bei Release-Closure (Mode A+B).
- `/consistency-check`: liest alle Invarianten aus dieser Datei und
 prueft sie. Ergebnisse landen in der Graph-Health-Sektion des
 Backlogs plus als FIX/IMPs.

## Abhaengigkeiten und Implementierungsreihenfolge

Jedes Artefakt (Epic, Feature, ADR, FIX, IMP) darf im Frontmatter
`depends-on:` als Liste von Artefakt-IDs fuehren. Semantik: "Dieses
Artefakt kann erst umgesetzt werden, wenn die gelisteten Artefakte
Phase `Released` erreicht haben."

**Frontmatter-Syntax:**

```yaml
depends-on: [FEAT-03-30, ADR-47]
```

**Regeln:**

- Referenzen zeigen auf existierende Artefakte (Invariante E-10).
- Der Graph der `depends-on`-Kanten ist azyklisch (E-11). Zyklen sind
 Konsistenz-Fehler und werden von `/consistency-check` gemeldet.
- Cross-Artefakt-Typen erlaubt: ein Feature kann auf eine ADR warten,
 eine IMP auf ein anderes Feature, ein Epic auf einen anderen Epic.
- Transitive Reihenfolge: wenn A auf B und B auf C wartet, ist C vor
 B vor A.

**Darstellung:**

- **Backlog**: Spalte `Abhaengig von` in jeder Feature-/FIX-/IMP-
 Tabelle. Eintrag als komma-separierte ID-Liste oder `-`.
- **Epic-/Feature-/ADR-Spezifikation**: eigener Abschnitt
 `## Abhaengigkeiten` im Body, der das Frontmatter-Feld spiegelt
 und kurz begruendet, warum die Abhaengigkeit existiert.
- **Graph-Viewer**: eigene Kanten-Art `depends-on` (eigene Farbe,
 gestrichelt). Topologische Reihenfolge kann als Layout-Option
 gewaehlt werden ("Implementierungs-Sequenz").
- **`/consistency-check`**: zeigt am Ende die topologisch sortierten
 Strata (Level 0 = keine unerfuellten Abhaengigkeiten, Level n = alle
 Abhaengigkeiten in Level < n).

## Artefakt-Triage am Einstiegspunkt (verbindlich fuer alle Skills)

**Regel:** Jede Aktivitaet, die Code, Doku oder Spezifikationen aendert,
ist vor der ersten inhaltlichen Arbeit einem Artefakt-Typ zuzuordnen.
Das gilt unabhaengig davon, welcher Skill den Einstieg bildet.

Minimal-Anforderung an den User (bzw. an den Skill, der das vom User
erfragt): Eine Antwort auf die Frage

> "Ist das, was du jetzt tust, ein neues Feature, eine Verbesserung
> (Improvement) an einem bestehenden Feature, oder ein Fix fuer einen
> Bug oder eine Drift?"

**Entscheidungsbaum (Skill wendet ihn ohne Rueckfrage an, wenn eindeutig):**

1. **Neuer Epic** (themenbreite Capability-Klammer):
   - **PFLICHT vorher:** Item-BA `analysis/BA-EPIC-{nn}-{slug}.md`
     via `/business-analysis`
   - dann **EPIC** anlegen unter
     `_devprocess/requirements/epics/EPIC-{nn}-{slug}.md`,
     Frontmatter `ba-ref:` zeigt auf die BA-Datei
   - `/requirements-engineering` uebernimmt

2. **Neue user-facing Capability** (Funktion, die es vorher nicht gab):
   - **PFLICHT vorher:** Item-BA `analysis/BA-FEAT-{ee}-{ff}-{slug}.md`
     via `/business-analysis` (Ausnahme: Feature ist vollstaendig
     durch die Epic-Item-BA gedeckt - Skill fragt einmal)
   - dann neues **FEATURE** anlegen, Pflicht-Bindung an ein Epic
   - Frontmatter traegt nur Identitaet und Relations
     (`id`, `epic`, `ba-ref`, optional `subtype` und
     `depends-on`). Kein Lifecycle-`status:` und kein `phase:`
     im Frontmatter (siehe N-10).
   - Backlog-Row mit `status: Ready, phase: Building`,
     `Prio: <P0|P1|P2|P3>`. Status, Phase und Priority leben
     ausschliesslich in der BACKLOG-Row.
   - `/requirements-engineering` uebernimmt

3. **Verbesserung an bestehendem Feature** (Refactor, Performance,
   Doku-Drift, zusaetzliche Tests, Konfig-Update, etc.):
   - **OPTIONAL vorher:** Mini-BA
     `analysis/BA-IMP-{ee}-{ff}-{nn}-{slug}.md` wenn Wert oder
     Scope unklar; sonst direkt das IMP-Artefakt
   - neues **IMP** unter
     `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md`
   - Frontmatter traegt nur Identitaet und Relations: `feature:`
     und `epic:` sind PFLICHT, `ba-ref:` falls BA existiert,
     optional `depends-on:`. Kein `status:`, kein `phase:`,
     kein `priority:` im Frontmatter (siehe N-15).
   - Backlog-Row mit `status: Ready, phase: Building`, plus
     `Prio: <P0|P1|P2|P3>`-Spalte. Diese drei Felder leben
     ausschliesslich in der BACKLOG-Row.

4. **Fix fuer einen beobachteten Bug oder eine Drift** (Symptom: etwas
   funktioniert nicht wie spezifiziert):
   - **OPTIONAL vorher:** Mini-BA
     `analysis/BA-FIX-{ee}-{ff}-{nn}-{slug}.md` wenn Root Cause
     oder Soll-Verhalten unklar; sonst direkt das FIX-Artefakt
   - neues **FIX** unter
     `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md`
   - Frontmatter `feature:` + `epic:` PFLICHT, `ba-ref:` falls
     BA existiert
   - kausale Kette im Body pflegen

5. **Architektur-Entscheidung**, die weitere Artefakte beeinflusst:
   - neue **ADR** (MADR-Format), verknuepft mit betroffenen Features
   - `/architecture` uebernimmt

**Kein Skill darf Code- oder Doku-Aenderungen ausfuehren, bevor diese
Zuordnung erfolgt ist.** Wenn die Zuordnung nicht eindeutig aus dem
User-Prompt ableitbar ist, stellt der Skill genau eine praegnante
Frage und setzt dann fort. Keine Diskussion, keine Optionen-Liste
ueber mehrere Entscheidungen.

**Ausnahmen:**

- Reine Leseoperationen (Recherche, Analyse, Reports) brauchen keine
  Triage.
- `/consistency-check` prueft und fixt bestehende Artefakte, erzeugt
  keine neuen.
- `/reverse-engineering` triagiert rueckwaertsgerichtet: existierender
  Code wird in Features, Epics, ADRs, FIXes, IMPs zerlegt.

**Wo der Einstieg triagiert wird:**

- `/dia-guide`: in der Hybrid-Entry-Detection direkt nach der
  Projektstand-Erkennung.
- `/business-analysis`: vor Phase 1, wenn der User direkt mit einer
  Feature-Idee kommt statt mit Problem/Persona.
- `/requirements-engineering`: am Start, wenn der User ohne BA-Bezug
  ein Feature vorschlaegt.
- `/architecture`: am Start, um zu pruefen ob die ADR-Idee ein Feature
  voraussetzt.
- `/coding`: **immer** vor dem ersten Edit. Ohne eindeutige Zuordnung
  wird die Triage-Frage gestellt.
- `/testing`: vor dem ersten neuen Test. Reine Test-Analyse (Coverage-
  Report, Lesen bestehender Tests) ist read-only und braucht keine
  Triage.

**Handoff-Durchreichung (gegen Mehrfach-Fragen):**

Die Triage-Zuordnung wird im ersten Handoff-Eintrag verankert und
danach von allen nachfolgenden Skills als gesetzt uebernommen. Format
und Regel: siehe `skills/dia-guide/SKILL.md` Abschnitt
"Handoff entry format". Pflichtfelder im Kopfblock: `triage:`,
`triage_kind:`; bei IMP und FIX zusaetzlich `feature:` und `epic:`.

## Aenderungs-Protokoll

Wer diese Datei aendert, muss `/consistency-check` Mode A
nachziehen, damit die neuen Invarianten auch wirklich geprueft werden.
Ohne Code-Update im Skill bleibt die Invariante nur dokumentiert,
nicht enforced.
