# Test-Anleitung: Merge-Hook gegen ID-Kollisionen

Ziel: Verifizieren, dass der `pre-merge-commit`-Hook und der
`scripts/merge-to-dev.sh`-Wrapper ID-Kollisionen zwischen parallelen
Feature-Branches korrekt erkennen, blocken bzw. auflösen.

Drei Akteure:

- `tools/renumber-for-merge.py` - Kernlogik (Konflikt-Detection,
  Mapping, Apply, mehrere Modi)
- `tools/git-hooks/pre-merge-commit` - Sicherheitsnetz, blockt
  Direktmerge bei Tree-Duplicate-IDs
- `scripts/merge-to-dev.sh` - Wrapper, der vor dem Merge auf der
  Source-Branch umnummeriert und committet, dann mergt

## Voraussetzungen

- macOS oder Linux mit `bash`, `git ≥ 2.30`, `python3 ≥ 3.10`
- Pfad zum DIA-Repo bekannt (im Folgenden `$DIA`):
  ```bash
  DIA=/Users/sebastianhanke/projects/digital-innovation-agents
  ```
- Ein leeres Test-Verzeichnis unter `/tmp` (wird angelegt)

## Test 1: Direktmerge wird vom Hook geblockt

**Erwartetes Verhalten:** Der Merge bricht ab, weil zwei Files
denselben EPIC-04-Slug-Stamm tragen. dev bleibt unverändert.

```bash
# 1. Test-Repo aufsetzen
rm -rf /tmp/dia-merge-test && mkdir -p /tmp/dia-merge-test
cd /tmp/dia-merge-test
git init -q -b main
git config user.email t@t && git config user.name t
mkdir -p _devprocess/{analysis,context,requirements/{epics,features,fixes,improvements}}
touch _devprocess/requirements/epics/.keep _devprocess/analysis/.keep
echo "# Backlog" > _devprocess/context/BACKLOG.md
git add -A && git commit -qm init

# 2. DIA-Hook + Renumber-Script installieren
cp $DIA/tools/git-hooks/pre-merge-commit .git/hooks/
chmod +x .git/hooks/pre-merge-commit
mkdir -p .git/hooks-data
cp $DIA/tools/renumber-for-merge.py .git/hooks-data/

# 3. dev: legt EPIC-04 (onboarding) an
git checkout -qb develop
printf -- '---\nid: EPIC-04\n---\n# EPIC-04\n' \
  > _devprocess/requirements/epics/EPIC-04-onboarding.md
echo "EPIC-04" > _devprocess/context/BACKLOG.md
git add -A && git commit -qm "dev: EPIC-04 onboarding"

# 4. feature/foo (off main): legt anderes EPIC-04 (billing) an
git checkout -qb feature/foo main
printf -- '---\nid: EPIC-04\n---\n# EPIC-04\n' \
  > _devprocess/requirements/epics/EPIC-04-billing.md
git add -A && git commit -qm "feature/foo: EPIC-04 billing"

# 5. Direktmerge versuchen
git checkout -q develop
git merge --no-ff -m "merge feature/foo direct" feature/foo
echo "exit code: $?"
git log --oneline --all --graph -5
```

**Pass-Kriterien:**

- Letzte Zeilen vom Merge-Output enthalten `Merge blocked: id collisions`
- `exit code: 1` (in manchen git-Versionen wird der Hookexit am Ende
  trotzdem als 0 gemeldet, dann zählt: kein neuer Merge-Commit auf dev)
- `git log --oneline --all --graph -5` zeigt **keinen** Merge-Commit
  auf dev. dev steht weiterhin auf dem `dev: EPIC-04 onboarding`-Commit.

## Test 2: Wrapper renumbert sauber und mergt durch

**Erwartetes Verhalten:** `scripts/merge-to-dev.sh` erzeugt einen
`chore(renumber): align ids with dev`-Commit auf feature/foo, mergt
dann sauber, dev hat danach EPIC-04 + EPIC-05 nebeneinander.

```bash
# Im selben /tmp/dia-merge-test
cd /tmp/dia-merge-test
git merge --abort 2>/dev/null
git branch -D dev-backup 2>/dev/null

# Wrapper laufen lassen
bash $DIA/scripts/merge-to-dev.sh feature/foo develop
echo "exit code: $?"

# Verifikation
git log --oneline --all --graph -8
ls _devprocess/requirements/epics/
```

**Pass-Kriterien:**

- Output enthält:
  - `[merge-to-dev] id collisions detected, renumbering source branch`
  - `Renumber plan (feature/foo -> aligned with dev): epic: EPIC-04 -> EPIC-05`
  - `[merge-to-dev] renumber commit landed on feature/foo`
  - `Merge made by the 'ort' strategy.`
  - `[merge-to-dev] merge complete`
- `exit code: 0`
- Git-Log zeigt einen Renumber-Commit auf feature/foo zwischen dem
  ursprünglichen feature-Commit und dem Merge-Commit auf dev.
- `_devprocess/requirements/epics/` enthält **beide** Files:
  `EPIC-04-onboarding.md` und `EPIC-05-billing.md`.

## Test 3: Idempotenz (zweiter Lauf ohne Kollision)

```bash
cd /tmp/dia-merge-test
# Branch nochmal mergen, soll No-op sein
git checkout -q feature/foo
git merge -q dev  # bring feature/foo up to date
python3 .git/hooks-data/renumber-for-merge.py --target dev --check-only
echo "check-only exit: $?  (0 = clean, 1 = collisions)"
```

**Pass-Kriterium:** `check-only exit: 0`.

## Test 4: FEAT- und FIX-Renaming inkl. Body-Refs

```bash
# Branch zuruecksetzen, dann komplexeres Setup
rm -rf /tmp/dia-merge-test2 && mkdir -p /tmp/dia-merge-test2
cd /tmp/dia-merge-test2
git init -q -b main
git config user.email t@t && git config user.name t
mkdir -p _devprocess/{analysis,context,requirements/{epics,features,fixes,improvements}}
touch _devprocess/requirements/epics/.keep _devprocess/analysis/.keep \
      _devprocess/requirements/features/.keep _devprocess/requirements/fixes/.keep
echo "# Backlog" > _devprocess/context/BACKLOG.md
git add -A && git commit -qm init
cp $DIA/tools/git-hooks/pre-merge-commit .git/hooks/
chmod +x .git/hooks/pre-merge-commit
mkdir -p .git/hooks-data
cp $DIA/tools/renumber-for-merge.py .git/hooks-data/

# dev: EPIC-04, FEAT-04-02, FIX-04-02-01
git checkout -qb develop
printf -- '---\nid: EPIC-04\n---\n' > _devprocess/requirements/epics/EPIC-04-onb.md
printf -- '---\nid: FEAT-04-02\nepic: EPIC-04\n---\n' \
  > _devprocess/requirements/features/FEAT-04-02-magic.md
printf -- '---\nid: FIX-04-02-01\nfeature: FEAT-04-02\nepic: EPIC-04\n---\n' \
  > _devprocess/requirements/fixes/FIX-04-02-01-bug.md
echo "EPIC-04, FEAT-04-02, FIX-04-02-01" > _devprocess/context/BACKLOG.md
git add -A && git commit -qm "develop"

# feature/bar (off main): kollidierendes EPIC-04 + FEAT-04-02 + FIX-04-02-01
git checkout -qb feature/bar main
printf -- '---\nid: EPIC-04\n---\n# EPIC-04\nrefers to FEAT-04-02\n' \
  > _devprocess/requirements/epics/EPIC-04-bill.md
printf -- '---\nid: FEAT-04-02\nepic: EPIC-04\n---\n# FEAT-04-02\nbody mentions EPIC-04 and FEAT-04-02\n' \
  > _devprocess/requirements/features/FEAT-04-02-checkout.md
printf -- '---\nid: FIX-04-02-01\nfeature: FEAT-04-02\nepic: EPIC-04\n---\n' \
  > _devprocess/requirements/fixes/FIX-04-02-01-tax.md
git add -A && git commit -qm "feature/bar"

# Wrapper laufen
bash $DIA/scripts/merge-to-dev.sh feature/bar develop
echo "exit: $?"

# Verifikation
ls _devprocess/requirements/epics/ _devprocess/requirements/features/ _devprocess/requirements/fixes/
echo "---"
cat _devprocess/requirements/features/FEAT-05-02-checkout.md
```

**Pass-Kriterien:**

- Renumber-Plan im Output:
  - `epic: EPIC-04 -> EPIC-05`
  - `feat: FEAT-04-02 -> FEAT-05-02`
  - `fix: FIX-04-02-01 -> FIX-05-02-01`
- Files heißen jetzt: `EPIC-05-bill.md`, `FEAT-05-02-checkout.md`,
  `FIX-05-02-01-tax.md` (auf feature/bar bzw. nach Merge in dev)
- Body von `FEAT-05-02-checkout.md` enthält `body mentions EPIC-05 and FEAT-05-02`
  (Body-Refs wurden mit-renamed)
- Frontmatter `epic: EPIC-05` und `id: FEAT-05-02` korrekt

## Test 5: Modi-Selbsttest des Renumber-Skripts

```bash
cd /tmp/dia-merge-test2

# --list-conflicts ohne Apply
git checkout -q develop
git reset -q --hard HEAD~1  # vor dem Merge
git checkout -q feature/bar
git reset -q --hard HEAD~1  # vor dem Renumber-Commit (falls vorhanden)
python3 $DIA/tools/renumber-for-merge.py --target dev --list-conflicts

# --check-only (Exit-Code-Sondierung)
python3 $DIA/tools/renumber-for-merge.py --target dev --check-only
echo "check-only exit: $?"  # erwartet: 1

# --dry-run (zeigt Plan, ändert nichts)
python3 $DIA/tools/renumber-for-merge.py --target dev --dry-run
git status --short  # sollte leer sein

# --check-tree-duplicates (post-merge state)
git checkout -q develop
git merge --no-ff -m "test" feature/bar 2>/dev/null  # kann blockieren
python3 $DIA/tools/renumber-for-merge.py --check-tree-duplicates
echo "tree-duplicates exit: $?"
```

**Pass-Kriterien:**

- `--list-conflicts` druckt JSON mit den Mappings, ohne Files zu ändern
- `--check-only` exit 1 bei Kollision, exit 0 ohne
- `--dry-run` lässt `git status --short` leer
- `--check-tree-duplicates` exit 1, wenn zwei Files dieselbe ID
  tragen (nach naivem Merge-Versuch sichtbar)

## Aufräumen

```bash
rm -rf /tmp/dia-merge-test /tmp/dia-merge-test2
```

## Bekannte Stolpersteine

- Das Test-Repo muss die Verzeichnisse `_devprocess/requirements/{epics,features,fixes,improvements}/`
  schon im `init`-Commit enthalten (per `.keep`-Files), sonst hat
  `feature/<branch>` (off main) diese Verzeichnisse nicht und das
  Setup schlägt fehl.
- Wenn das Test-Repo BACKLOG.md auf beiden Seiten ändert, gibt es
  einen normalen Three-Way-Markdown-Konflikt im Merge. Der ist
  unabhängig vom ID-Konflikt und muss manuell aufgelöst werden.
  Test 1 oben hält BACKLOG einfach, um den ID-Konflikt zu
  isolieren. Bei Test 4 schreibt feature/bar bewusst kein BACKLOG-
  Update, deshalb läuft der Merge sauber.
- macOS-Bash ist v3, `git`-Hook funktioniert trotzdem. Falls der
  Hook nicht greift: `ls -la .git/hooks/pre-merge-commit` prüfen
  (executable bit gesetzt? Shebang `#!/usr/bin/env bash` erste Zeile?).
- `MERGE_HEAD` existiert bei `pre-merge-commit` nicht zuverlässig.
  Der Hook prüft deshalb `--check-tree-duplicates` (zwei Files mit
  gleicher ID), nicht source-vs-target via MERGE_HEAD. Das ist
  Absicht.

## Was ein Bug aussieht

- Hook lässt Direktmerge in Kollision durch: hook nicht installiert,
  oder `pre-merge-commit` heißt falsch. Prüfen via
  `bash -x .git/hooks/pre-merge-commit` direkt nach `git merge --no-commit`.
- Wrapper renumbert, aber Merge bricht trotzdem ab: hook + script
  out of sync. Beide neu kopieren aus DIA-Repo.
- Renumber benennt Files um, aber Body-Refs bleiben alt: Pass-2-Sweep
  im Skript funktioniert nicht. Reproduzieren mit `--dry-run --list-conflicts`
  und das JSON gegen die Body-Inhalte halten.
