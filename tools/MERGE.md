# Merge-Workflow: ID-Alignment vor dem Merge

In Repos mit DIA-Artefakten (`EPIC-NN`, `FEAT-EE-FF`, `IMP-EE-FF-NN`,
`FIX-EE-FF-NN` plus die zugehoerigen Item-BAs in `analysis/`)
allokieren parallele Feature-Branches unabhaengig voneinander IDs.
Mergt man zwei Branches, die je `EPIC-04` (oder `FEAT-04-02`)
eingefuehrt haben, kollidieren die IDs.

DIA loest das mit drei kooperierenden Komponenten:

| Komponente | Datei | Zweck |
|------------|-------|-------|
| Renumber-Engine | `tools/renumber-for-merge.py` | Liest Target-Backlog, errechnet Mapping, fuehrt Renames + Body-Updates aus |
| Wrapper | `scripts/merge-to-dev.sh` | Renumbert Source-Branch, committet `chore(renumber)`, fuehrt Merge aus |
| Sicherheitsnetz | `tools/git-hooks/pre-merge-commit` | Blockt Direktmerge bei Tree-Duplicate-IDs |

## Installation

```bash
# Im Target-Projekt einmalig:
bash <DIA-repo>/tools/install-git-hooks.sh
```

Installiert beide Hooks (`pre-commit` und `pre-merge-commit`) plus
die Skripte unter `.git/hooks-data/`. Direkt aus dem DIA-Repo
funktioniert auch:

```bash
bash <DIA-repo>/scripts/merge-to-dev.sh feature/foo develop
```

(Der Wrapper findet das Skript ueber den `tools/`-Pfad oder
ueber `.git/hooks-data/` als Fallback.)

## Canonical Path: ueber den Wrapper mergen

```bash
bash scripts/merge-to-dev.sh <source-branch> [<target-branch>]
# Default target: develop
```

Was passiert:

1. Snapshot: `<target>` -> `<target>-backup` (lightweight branch)
2. Wechsel auf `<source-branch>`
3. `tools/renumber-for-merge.py --target <target> --check-only`
4. Wenn Kollisionen: Renumber-Apply, Auto-Commit
   `chore(renumber): align ids with <target> before merge`
5. Wechsel auf `<target>`
6. `git merge --no-ff <source-branch>`

Rollback bei Bedarf:

```bash
git checkout <target>
git reset --hard <target>-backup
```

## Direktmerge: was passiert dann?

```bash
git checkout develop
git merge --no-ff feature/foo
```

Der `pre-merge-commit`-Hook scannt das Working-Tree nach
duplicate IDs (zwei artifact files mit demselben ID-Stamm).
Bei Kollision: `exit 1`, Merge wird nicht committet, Hinweis-
Text:

```
Merge blocked: id collisions between the merging branch and dev.
Use the canonical merge path so ids are renumbered on the source
branch before the merge:
    git merge --abort
    git checkout <source-branch>
    bash scripts/merge-to-dev.sh <source-branch> develop
```

Bypass per `git merge --no-verify` ist moeglich, sollte aber nur
mit klarem Grund verwendet werden.

## Was alles renumbert wird

Per Mapping (alte ID -> neue ID) werden umgeschrieben:

- **Datei-Namen** in
  `_devprocess/requirements/{epics,features,fixes,improvements}/`
- **Datei-Namen** der korrespondierenden Item-BAs in
  `_devprocess/analysis/BA-{EPIC,FEAT,IMP,FIX}-*.md`
- **Frontmatter-Felder**: `id`, `epic`, `feature`, `ba-ref`,
  `depends-on`, `feature-refs`, `adr-refs`, `supersedes`,
  `superseded-by`, `target-id`, `parent-feat`
- **Body-Refs** in jedem `*.md` unter `_devprocess/`
- **`src/ARCHITECTURE.map`** (wayfinder)
- **`FIXME(stub):`-Marker** im Source-Tree
  (siehe graph-invariants E-14)

**Nicht renumbert:**

- ADRs und PLANs (eigene Nummerierung, semantisch entkoppelt)
- `_devprocess/context/HANDOFFS.md` (append-only audit trail)

## Mapping-Regel

Pro Klasse wird die naechste freie ID aus dem Target-Backlog
ermittelt:

- **EPIC**: nach `max(target.EPIC) + 1`
- **FEAT**: epic-lokal, neue `ee` aus EPIC-Mapping, neues `ff`
  als naechstes freies innerhalb des neuen Epics
- **IMP/FIX**: feature-lokal, neue `ee`/`ff` aus FEAT-Mapping,
  neues `nn` als naechstes freies innerhalb des neuen Features

Die Reihenfolge ist deterministisch: erst EPIC, dann FEAT (zieht
EPIC-Remap mit), dann IMP/FIX (zieht FEAT-Remap mit). Damit hat
jede Source-ID genau eine Ziel-ID.

## Modi des Renumber-Skripts

| Modus | Zweck |
|-------|-------|
| `--check-only` | Exit 1 bei Kollision, sonst 0. Kein Output. Fuer Hooks. |
| `--list-conflicts` | Druckt das Mapping als JSON. Kein Apply. |
| `--dry-run` | Berechnet Mapping, druckt Plan, schreibt nichts. |
| `--check-tree-duplicates` | Scant Working-Tree auf zwei Files mit gleicher ID. Pre-merge-commit hook nutzt diesen Modus. |
| `--source-ref <ref>` | Source-IDs aus einem git-ref lesen statt aus Working-Tree. Nur kombinierbar mit den read-only Modi oben. |
| (default) | Berechnet Mapping, schreibt Renames + Updates. |

## Edge Cases

### Source-Branch identisch zu Target an einer Stelle

Wenn beide Branches dieselbe Datei mit derselben ID anlegen
(gleicher Slug, gleicher Inhalt), produziert git keinen Konflikt
und das Renumber-Skript erkennt kein duplicate. Korrekt. Beispiel:
beide Branches mergen einen gemeinsamen Vorlauf-Commit.

### BACKLOG.md hat Three-Way-Konflikt

Wenn beide Branches `BACKLOG.md` modifiziert haben, gibt es einen
normalen Markdown-Konflikt. Der ist orthogonal zum ID-Konflikt
und muss manuell aufgeloest werden. Das Renumber-Skript laeuft
trotzdem (es schreibt eine konsolidierte BACKLOG.md auf dem
Source-Branch vor dem Merge), aber bei Konflikt-Markern
`<<<<<<<` im File scheitert der spaetere Merge.

Empfehlung: vor dem Wrapper-Lauf den Source-Branch via `git pull`
oder `git rebase dev` aktuell halten, damit BACKLOG.md kein
Konflikt mehr ist.

### Branch ohne `_devprocess/`

Skript: "No `_devprocess/` found; nothing to renumber." (exit 0).
Hook: lasst durch.

### Andere parallele Branches in der Pipeline

Beim Mergen von Branch A nach dev wird nur Branch A umgenummert.
Branch B (parallel) bleibt unangetastet. Beim spaeteren Merge von
B kann erneut eine Kollision auftreten, der dann durch den
naechsten Wrapper-Lauf fuer Branch B aufgeloest wird.

`/dia-migration` Phase 8 und `/reverse-engineering` Phase 9
listen alle parallelen Branches mit Kollisionsstand auf, damit
der Maintainer pro Branch entscheiden kann.

## Test

Manuelle Verifikation: `tools/test-merge-hook.md`. Fuehrt fuenf
End-to-End-Szenarien gegen ein temp-Repo unter `/tmp` aus
(Direktmerge-Block, Wrapper-Pfad, Idempotenz, FEAT/FIX-Renaming,
Modi-Selbsttest).

## Bypass-Regeln

- `git merge --no-verify` umgeht den `pre-merge-commit`-Hook.
  Akzeptabel bei: gezielter Hotfix, der nicht renumbert werden
  darf (z.B. Notfall-FIX, der den ID-Wert bewahren muss).
- Skript-Override per Umgebungsvariable existiert bewusst nicht.
  Der explizite Hook-Bypass ist die einzige Eskalation.

## Bekannte Stolpersteine

- `pre-merge-commit` feuert nur bei tatsaechlichen Merge-Commits,
  nicht bei Fast-Forward-Merges. Wenn der Source-Branch direkt
  vor dem Target-Tip liegt, wird kein Hook ausgefuehrt. Lösung:
  `git merge --no-ff` oder `scripts/merge-to-dev.sh` (forciert
  einen Merge-Commit).
- `MERGE_HEAD` existiert beim `pre-merge-commit`-Hook nicht
  zuverlaessig (haengt von Merge-Strategie und git-Version ab).
  Der Hook prueft deshalb mit `--check-tree-duplicates`, nicht
  per `--source-ref MERGE_HEAD`.
- Auf macOS-bash (3.x) funktioniert alles, aber `set -e` Verhalten
  in `if !`-Konstrukten kann Subtilitaeten haben. Bei Hook-
  Problemen: `bash -x .git/hooks/pre-merge-commit` direkt nach
  `git merge --no-commit` aufrufen, um den Trace zu sehen.
