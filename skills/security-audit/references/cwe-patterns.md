# CWE Analyse-Patterns fuer SAST

Systematische Grep/Analyse-Patterns pro CWE-Kategorie.

## CWE-79: Cross-Site Scripting (XSS)

Suche nach: `innerHTML`, `outerHTML`, `dangerouslySetInnerHTML`, `document.write`
Kontext: User-Input der ungefiltert in DOM geschrieben wird

## CWE-94: Code Injection

Suche nach: `eval()`, `new Function()`, `vm.runInNewContext`, `vm.runInThisContext`
Kontext: Dynamische Code-Ausfuehrung mit variablem Input

## CWE-78: Command Injection

Suche nach: `exec()`, `spawn()`, `execSync()`, `child_process`
Kontext: Shell-Kommandos mit User-Input ohne Escaping

## CWE-22: Path Traversal

Suche nach: Pfad-Konstruktion mit `+` oder Template Literals, `../`
Kontext: Fehlende Pfad-Normalisierung, kein `path.resolve()` + Prefix-Check

## CWE-918: Server-Side Request Forgery (SSRF)

Suche nach: `fetch()`, `requestUrl()`, `axios`, `http.get` mit variablem URL
Kontext: URL aus User-Input ohne Allowlist-Pruefung

## CWE-1321: Prototype Pollution

Suche nach: `Object.assign({}, userInput)`, `{...userInput}`, `lodash.merge`
Kontext: Deep-Merge oder Spread auf unvalidiertem User-Input

## CWE-400: Regular Expression Denial of Service (ReDoS)

Suche nach: `new RegExp(userInput)`, verschachtelte Quantifier `(a+)+`
Kontext: Regex mit User-Input oder katastrophisches Backtracking

## CWE-312: Sensitive Data Exposure

Suche nach: `console.log` mit Token/Key/Password, API-Keys im Source Code
Kontext: Credentials in Logs oder Quellcode statt Environment Variables

## CWE-502: Insecure Deserialization

Suche nach: `JSON.parse()` ohne Schema-Validierung, `yaml.load()`, `pickle.loads()`
Kontext: Deserialisierung von nicht vertrauenswuerdigem Input

## CWE-863: Authorization Bypass

Suche nach: Fehlende Access Control Checks, Rollen-Pruefung nur im Frontend
Kontext: API-Endpunkte ohne Server-seitige Autorisierung

## Finding-Format

Fuer jeden Fund:

```markdown
### {Severity}-{N}: {Titel} ({CWE}-{ID})

| Field | Value |
|-------|-------|
| **Severity** | Critical / High / Medium / Low / Info |
| **CWE** | CWE-{ID} |
| **Location** | `src/path/file.ts:{line}` |
| **Status** | Confirmed / Mitigated / False Positive |

**Finding:** {Was wurde gefunden}
**Risk:** {Welches Risiko besteht}
**Remediation:** {Wie beheben}

**Code-Vorschlag:**
- {unsicherer Code}
+ {sicherer Code}
```
