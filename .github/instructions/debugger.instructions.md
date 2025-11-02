---
applyTo: "logs/**/*.md, src/**/*.*, tests/**/*.*"
description: "Automatische Validierungs- und Qualitätsregeln für Debugging"
autoLoad: true
---

# Debugger - Validation & Quality Rules

Diese Instructions werden **automatisch** angewendet beim Arbeiten mit Error Logs und Debugging. Sie ergänzen den Debugger Chatmode mit spezifischen Validierungs- und Quality-Checks.

> **Wichtig:** Diese Regeln gelten zusätzlich zu `.github/chatmodes/debugger.chatmode.md`

## 📁 Unterstützte Dateitypen

Diese Validierungsregeln greifen bei:

```
✅ logs/ERROR-TASK-*.md (Error Logs)
✅ src/**/*.* (Source Code - beim Fixen - all languages)
✅ tests/**/*.* (Test Files - beim Aktualisieren - all languages)
✅ Beliebige Code-Dateien beim Debugging (Python, JS/TS, Java, Go, C#, etc.)
```

---

## 🔍 Automatische Validierungen

### 1. Error Log Format Validation

**Pattern-Validierung beim Lesen:**

```javascript
// Automatischer Check
const errorLogPattern = /^ERROR-TASK-\d{3}-\d{3}-\d{4}-\d{2}-\d{2}-\d{4}\.md$/;

// Beispiel:
// ERROR-TASK-001-001-2025-10-07-1430.md
```

**Required Sections im Error Log:**

```markdown
MANDATORY Sections (beim Lesen):

✅ ## Task Information
   - Task ID
   - Task Title  
   - Date
   - Developer

✅ ## Error Summary
   - Failed Tests count
   - Test Type
   - Severity

✅ ## Test Failures
   Für jeden Test:
   - Test Name
   - File Path
   - Status
   - Error Message
   - Stack Trace
   - Context

✅ ## Code Context
   - Implementation File
   - Relevant Code Section
   - Test Code

✅ ## Environment Information
   - Language/Runtime Version
   - Test Framework
   - Dependencies
   - System

✅ ## Attempted Solutions (optional)
   - What was tried
   - Results
```

**Fehlermeldung bei ungültigem Error Log:**

```
❌ Error Log Format ungültig

Datei: logs/error-task-1.md
Problem: Dateiname entspricht nicht Pattern

Korrekt wäre: ERROR-TASK-001-001-2025-10-07-1430.md

Format:
  ERROR-TASK-{FEATURE-ID}-{TASK-NUM}-{YYYY-MM-DD}-{HHMM}.md
  
Beispiel:
  ERROR-TASK-001-001-2025-10-07-1430.md
```

**Fehlermeldung bei fehlenden Sections:**

```
❌ Error Log unvollständig

Datei: ERROR-TASK-001-001-2025-10-07-1430.md
Status: 4/6 Required Sections vorhanden

Fehlende Sections:
  ❌ ## Code Context
  ❌ ## Environment Information

Action erforderlich:
  Developer muss Error Log vervollständigen.
  Debugger kann nicht ohne vollständige Info arbeiten.
  
Template: .github/templates/ERROR-LOG-TEMPLATE.md
```

---

### 2. Root Cause Analysis Validation

**Mandatory Analysis Documentation:**

```markdown
CHECK während Phase 2:

✅ Stack Trace Analysis vorhanden?
✅ Code Inspection dokumentiert?
✅ Test Analysis dokumentiert?
✅ Root Cause Category assigned?
✅ Root Cause != Symptom?
✅ Impact Analysis vorhanden?

VERBOTEN:
❌ "Error is in line X" ohne Erklärung WARUM
❌ "Fix is to change Y" ohne Root Cause
❌ Symptom-Beschreibung statt Root Cause
❌ Vage Aussagen wie "something is wrong"
```

**Root Cause Analysis Document Format:**

```markdown
# Root Cause Analysis: TASK-XXX

## Error Summary
- **Test:** [specific test name]
- **Error:** [specific error type and message]
- **Category:** [Logic Error | Type Error | etc.]

## Stack Trace Analysis
1. Error originated in: [file:line]
2. Function called from: [file:line]
3. Propagated through: [call chain]

## Root Cause
**THE REAL PROBLEM:**
[Clear, specific explanation of WHY error occurs]
[Not WHAT error is, but WHY it happens]

**Why Developer's Fix Didn't Work:**
[If applicable, explain why attempted fix failed]

## Impact Analysis
- Affects: [scope of impact]
- Severity: [High | Medium | Low]
- Regression Risk: [High | Medium | Low]
```

**Fehlermeldung bei schlechter Analyse:**

```
⚠️ Root Cause Analysis unzureichend

Datei: ROOT-CAUSE-ANALYSIS-TASK-XXX.md
Probleme gefunden: 3

1. ❌ Root Cause zu vage
   Gefunden: "Error in function"
   Benötigt: Spezifische Erklärung WARUM Fehler auftritt
   
   Beispiel (gut):
   "Function doesn't handle discount=None case. When None 
    is passed, it attempts arithmetic on None, causing TypeError."

2. ❌ Missing Stack Trace Analysis
   Section existiert, aber enthält nur "Error in line 45"
   Benötigt: Vollständige Call-Chain-Analyse
   
3. ❌ Root Cause = Symptom
   Gefunden: "Test fails with AssertionError"
   Problem: Das ist der Symptom, nicht Root Cause
   Benötigt: WARUM kommt es zu diesem AssertionError?

Action erforderlich:
  Vertiefe Analyse:
  1. Lies Stack Trace von BOTTOM nach TOP
  2. Identifiziere ERSTE Fehlerquelle
  3. Erkläre WARUM Code dort versagt
  4. Unterscheide Symptom vs Root Cause
```

---

### 3. Fix Strategy Validation

**Mandatory Strategy Documentation:**

```markdown
CHECK während Phase 3:

✅ Mindestens 2 Options betrachtet?
✅ Chosen Option mit Rationale?
✅ Test Strategy definiert?
✅ Regression Prevention geplant?
✅ Implementation Steps klar?

VERBOTEN:
❌ Nur eine Option ohne Alternativen
❌ "Quick fix" ohne Strategie
❌ Workaround als "Fix"
❌ Keine Test Strategy
```

**Fix Strategy Document Format:**

```markdown
# Fix Strategy: TASK-XXX

## Root Cause (Recap)
[One-line summary from Phase 2]

## Proposed Fix
**Option 1: [Name] (CHOSEN)**
```python
[Code example]
```

**Why Option 1:**
- [Reason 1]
- [Reason 2]

**Option 2: [Name]**
```python
[Code example]
```

**Why NOT Option 2:**
- [Reason 1]
- [Reason 2]

## Test Strategy
1. [Test update/addition 1]
2. [Test update/addition 2]

## Regression Prevention
- [Prevention measure 1]
- [Prevention measure 2]

## Implementation Steps
1. [Step 1]
2. [Step 2]
```

**Fehlermeldung bei schlechter Strategie:**

```
❌ Fix Strategy unvollständig

Datei: FIX-STRATEGY-TASK-XXX.md
Status: 3/5 Required Sections vorhanden

Probleme:

1. ❌ Nur eine Option
   Gefunden: Option 1 only
   Benötigt: Min. 2 Options mit Pros/Cons
   
   → Betrachte Alternativen:
     - Default Parameter
     - Explicit None Handling
     - Validation at API Layer
     - Type Narrowing

2. ❌ Test Strategy fehlt
   Keine Test-Planung dokumentiert
   
   → Definiere:
     - Welche Tests zu aktualisieren?
     - Welche Tests neu hinzuzufügen?
     - Edge Cases abzudecken?

3. ❌ Regression Prevention fehlt
   Keine Maßnahmen gegen Regressionen
   
   → Plane:
     - ALL tests run
     - Coverage check
     - Integration test verification

Action erforderlich:
  Vervollständige Fix Strategy vor Implementation!
```

---

### 4. Fix Implementation Quality

**Code Quality Checks:**

```markdown
CHECK während Phase 4:

✅ Type Hints vorhanden?
✅ Docstrings aktualisiert?
✅ Input Validation hinzugefügt?
✅ Error Handling proper?
✅ No Workarounds?
✅ Clean Code Principles?
✅ No TODOs in Fix?

VERBOTEN:
❌ try-catch ohne proper logging
❌ Hardcoded values
❌ Magic numbers
❌ Commented-out code
❌ print() statements (use logging)
```

**Beispiel - SCHLECHTER Fix:**

```python
# ❌ BAD FIX
def calculate_price(base, discount):
    try:
        return base - (base * discount)  # No validation
    except:  # Bare except
        return 0  # Loses information
```

**Beispiel - GUTER Fix:**

```python
# ✅ GOOD FIX
def calculate_price(
    base_price: float,  # Type hint
    discount: float = 0.0  # Default parameter
) -> float:  # Return type hint
    """
    Calculate final price with optional discount.
    
    Args:
        base_price: Original price (must be positive)
        discount: Discount percentage 0-100 (default: 0.0)
        
    Returns:
        Final price after discount
        
    Raises:
        ValueError: If inputs invalid
        
    Examples:
        >>> calculate_price(100.0, 10.0)
        90.0
    """
    # Input validation
    if base_price < 0:
        raise ValueError("Base price must be positive")
    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")
    
    # Clean calculation
    return base_price * (1 - discount / 100)
```

**Fehlermeldung bei schlechtem Fix:**

```
⚠️ Fix Implementation Quality Issues

Datei: src/pricing.py
Function: calculate_price
Probleme: 4

1. ❌ Missing Type Hints
   Gefunden: def calculate_price(base, discount):
   Fix: def calculate_price(base_price: float, discount: float = 0.0) -> float:

2. ❌ No Input Validation
   Problem: Function accepts any value without checking
   Fix: Add validation for negative/invalid inputs

3. ❌ Bare except clause
   Gefunden: except:
   Fix: except SpecificException as e: + proper logging

4. ❌ Missing Docstring
   Problem: No documentation for function behavior
   Fix: Add comprehensive docstring with examples

Action erforderlich:
  Refactor Fix gemäß Clean Code Principles.
  Siehe Best Practice Examples in debugger.chatmode.md
```

---

### 5. Test Update/Addition Validation

**Test Quality Checks:**

```markdown
CHECK während Phase 4:

✅ Affected tests updated?
✅ Edge case tests added?
✅ Happy path tested?
✅ Error cases tested?
✅ Parametrized tests für multiple scenarios?
✅ Test names descriptive?
✅ Docstrings in tests?

MINIMUM Test Coverage:
✅ 1x Happy Path Test
✅ 1x Edge Case Test
✅ 1x Error Case Test
✅ 1x Parametrized Test (if applicable)
```

**Test Quality Example - BAD:**

```python
# ❌ BAD TESTS
def test_price():
    assert calculate_price(100, 10) == 90
    
def test_price2():
    assert calculate_price(100) == 100
```

**Test Quality Example - GOOD:**

```python
# ✅ GOOD TESTS
class TestPriceCalculation:
    """Tests for price calculation with discount."""
    
    def test_price_with_valid_discount(self):
        """Test normal discount application."""
        result = calculate_price(100.0, 10.0)
        assert result == 90.0
    
    def test_price_without_discount_parameter(self):
        """Test default discount behavior."""
        result = calculate_price(100.0)
        assert result == 100.0
    
    def test_price_with_zero_discount(self):
        """Test explicit zero discount."""
        result = calculate_price(100.0, 0.0)
        assert result == 100.0
    
    def test_price_with_invalid_negative_discount(self):
        """Test error handling for negative discount."""
        with pytest.raises(ValueError, match="between 0 and 100"):
            calculate_price(100.0, -10.0)
    
    @pytest.mark.parametrize("base,discount,expected", [
        (100.0, 10.0, 90.0),
        (100.0, 20.0, 80.0),
        (50.0, 50.0, 25.0),
    ])
    def test_various_discount_scenarios(self, base, discount, expected):
        """Test multiple discount scenarios."""
        assert calculate_price(base, discount) == expected
```

**Fehlermeldung bei unzureichenden Tests:**

```
⚠️ Test Coverage unzureichend

Datei: tests/unit/test_pricing.py
Function: calculate_price
Probleme: 3

1. ❌ Nur 2 Tests für Fix
   Gefunden: test_price, test_price2
   Minimum: 4 Tests (Happy, Edge, Error, Parametrized)
   
   Fehlende Tests:
   - test_price_with_invalid_discount()
   - test_price_with_boundary_values()
   - test_various_discount_scenarios() (parametrized)

2. ❌ Test Namen nicht beschreibend
   test_price, test_price2 sind zu generisch
   
   → Nutze beschreibende Namen:
     test_price_with_valid_discount
     test_price_without_discount_parameter

3. ❌ Keine Docstrings in Tests
   Tests sollten dokumentieren WAS sie testen
   
   → Füge Docstrings hinzu:
     """Test normal discount application."""

Action erforderlich:
  Erweitere Test Suite um fehlende Cases.
  Minimum: 4 Tests mit klaren Namen und Docstrings.
```

---

### 6. Comprehensive Testing Validation (CRITICAL)

**MANDATORY: ALL Tests müssen ausgeführt werden!**

```markdown
CHECK während Phase 5:

✅ Affected tests run?
✅ ALL unit tests run?
✅ ALL integration tests run?
✅ Coverage check run?
✅ Linter run?
✅ Type checker run (if applicable)?
✅ NO new failures?
✅ Coverage maintained (>90%)?

VERBOTEN:
❌ Nur betroffene Tests run
❌ Skip integration tests
❌ Ignore coverage drop
❌ "Tests probably pass"
❌ Proceed without running ALL tests
```

**Test Execution Evidence Required:**

```bash
# Evidence Format (in Resolution)
Test Results:
✅ Unit Tests: 134/134 passed (+7 new)
✅ Integration Tests: 45/45 passed
✅ Coverage: 94% (maintained, was 92%)
✅ Linter: 0 issues
✅ Type Check: Success (if applicable)

Test Commands Run:
[Adapt to your stack - see developer.chatmode.md for commands]
```

**Fehlermeldung bei unvollständigem Testing:**

```
❌ CRITICAL: Comprehensive Testing nicht durchgeführt

Problem: Nur affected tests wurden run

MANDATORY Requirements:
- [ ] ❌ ALL unit tests run
- [ ] ❌ ALL integration tests run
- [ ] ❌ Coverage check performed
- [x] ✅ Affected tests run (insufficient!)

Action erforderlich:
  Run COMPLETE test suite:
  
  1. Run ALL unit tests
  2. Run ALL integration tests
  3. Run coverage check
  4. Verify NO new failures
  5. Verify coverage maintained (>90% or project threshold)

UNTIL ALL tests run, fix is NOT validated!
```

**Regression Detection:**

```markdown
CHECK für Regressions:

✅ Alle bisherigen Tests noch passing?
✅ Keine neuen Failures?
✅ Coverage nicht gesunken?
✅ Keine Breaking Changes?

Wenn Regression gefunden:
❌ STOP immediately
❌ DO NOT proceed to Phase 6
❌ Analyze regression cause
❌ Fix regression
❌ Re-run ALL tests (Phase 5 again)
```

**Fehlermeldung bei Regression:**

```
❌ REGRESSION DETECTED!

Phase 5 Test Results:
- Unit Tests: 132/134 passed (2 NEW FAILURES!)
- Failed Tests:
  * test_order_total_calculation ❌
  * test_checkout_flow ❌

Analysis:
Both failures related to calculate_price() signature change.
Dependent functions calling with positional args now fail.

Impact: HIGH - Breaks order processing

Action erforderlich:
1. STOP current fix process
2. Analyze regression cause:
   - Search ALL callers of calculate_price()
   - Identify breaking changes
3. Fix regression:
   - Update callers to use named parameters OR
   - Maintain backward compatibility
4. Re-run Phase 5 (ALL tests)
5. Only proceed to Phase 6 if ALL tests pass

DO NOT proceed without fixing regression!
```

---

### 7. Error Log Resolution Validation

**Resolution Section Required:**

```markdown
CHECK am Ende von Phase 6:

✅ Resolution Section im Error Log?
✅ Status: RESOLVED gesetzt?
✅ Root Cause dokumentiert?
✅ Fix Applied mit Code dokumentiert?
✅ Tests Updated dokumentiert?
✅ Test Results dokumentiert?
✅ Learnings dokumentiert?
✅ Prevention Strategy dokumentiert?
✅ Verification Checklist complete?

Resolution Section Format:
---
## ✅ RESOLUTION

**Status:** RESOLVED
**Resolved By:** Debugger Mode
**Resolution Date:** YYYY-MM-DD HH:MM
**Time to Resolve:** XX minutes

### Root Cause
[Clear explanation]

### Fix Applied
**File:** [path]
**Changes:** [list]
**Code:** [code block]

### Tests Updated
**File:** [path]
**Added/Updated Tests:** [list]
**Test Results:** [results]

### Learnings
1. [Learning 1]
2. [Learning 2]

### Prevention Strategy
- [Strategy 1]
- [Strategy 2]

### Verification
- [x] Original error resolved
- [x] All tests passing
- [x] No regressions
- [x] Coverage maintained
```

**Fehlermeldung bei unvollständiger Resolution:**

```
❌ Error Log Resolution unvollständig

Datei: ERROR-TASK-001-001-2025-10-07-1430.md
Status: 6/9 Resolution Sections vorhanden

Fehlende Sections:
  ❌ ### Prevention Strategy
  ❌ ### Verification Checklist
  ❌ ### Learnings

Action erforderlich:
  Vervollständige Resolution Section:
  
  1. Dokumentiere Learnings:
     Was haben wir aus diesem Fehler gelernt?
  
  2. Dokumentiere Prevention Strategy:
     Wie verhindern wir ähnliche Fehler zukünftig?
  
  3. Complete Verification Checklist:
     - [ ] Original error resolved
     - [ ] All tests passing
     - [ ] No regressions
     - [ ] Coverage maintained
     - [ ] Documentation updated

Resolution ist NICHT complete ohne diese Sections!
```

---

### 8. Commit Message Validation

**Commit Message Format Required:**

```markdown
CHECK vor Commit:

✅ Type correct? (fix|docs|test)
✅ Scope present? (module/component)
✅ Root Cause documented?
✅ Fix Applied documented?
✅ Testing documented?
✅ References Error Log?
✅ Time to Fix documented?

Format:
fix(scope): brief description

Root Cause:
- Point 1
- Point 2

Fix Applied:
- Change 1
- Change 2

Testing:
- Test results
- Coverage info

Resolves: ERROR-TASK-XXX-YYYY-MM-DD-HHMM
Related: TASK-XXX
Time to Fix: XX minutes
```

**Beispiel - SCHLECHTE Commit Message:**

```
❌ BAD:
"fixed bug"

Problem: Keine Information!
```

**Beispiel - GUTE Commit Message:**

```
✅ GOOD:
fix(pricing): handle optional discount parameter correctly

Root Cause:
- calculate_price() didn't handle discount=None
- Missing input validation
- No default parameter

Fix Applied:
- Added default parameter: discount=0.0
- Added type hints for clarity
- Added input validation (0-100 range)
- Added proper error handling

Testing:
- Added 7 new test cases
- All edge cases covered
- 134/134 tests passing
- Coverage maintained at 94%

Resolves: ERROR-TASK-001-001-2025-10-07-1430
Related: TASK-001-001
Time to Fix: 45 minutes
```

**Fehlermeldung bei schlechter Commit Message:**

```
⚠️ Commit Message unzureichend

Gefunden: "fixed bug"

Probleme:
1. ❌ Kein Typ (fix|docs|test)
2. ❌ Kein Scope
3. ❌ Kein Root Cause
4. ❌ Kein Fix Applied
5. ❌ Keine Testing Info
6. ❌ Keine References

Action erforderlich:
  Schreibe informative Commit Message:
  - WAS war das Problem? (Root Cause)
  - WIE wurde es gelöst? (Fix Applied)
  - WIE wurde es validiert? (Testing)
  - WELCHER Error Log? (References)

Template: .github/templates/COMMIT-MESSAGE-TEMPLATE.txt
```

---

## 📊 Quality Gate Checks

**Pre-Commit Validation:**

```markdown
QGD (Quality Gate Debugging) Check:

✅ Error Log vollständig gelesen?
✅ Root Cause Analysis vollständig?
✅ Fix Strategy mit 2+ Options?
✅ Fix Implementation clean?
✅ Tests updated/added (min. 4)?
✅ ALL Tests run und passing?
✅ Coverage maintained (>90%)?
✅ NO Regressions?
✅ Error Log Resolution complete?
✅ Commit Message informative?

Wenn ALLE ✅:
  → Commit allowed
  → Notify Developer

Wenn EIN ❌:
  → BLOCK Commit
  → Show specific failure
  → Require fix
```

**Quality Gate Report Format:**

```
🔍 QGD (Quality Gate Debugging) Check

┌────────────────────────────────────────┐
│ Phase 1: Error Log Analysis           │
│ ✅ Error Log format valid              │
│ ✅ All required sections present       │
│ ✅ Context fully understood            │
├────────────────────────────────────────┤
│ Phase 2: Root Cause Analysis          │
│ ✅ Stack Trace analyzed                │
│ ✅ Root Cause identified (not symptom) │
│ ✅ Impact Assessment complete          │
├────────────────────────────────────────┤
│ Phase 3: Fix Strategy                 │
│ ✅ 2+ Options considered               │
│ ✅ Best option chosen with rationale   │
│ ✅ Test Strategy defined               │
├────────────────────────────────────────┤
│ Phase 4: Implementation                │
│ ✅ Fix implemented cleanly             │
│ ✅ Type hints added                    │
│ ✅ Input validation added              │
│ ✅ Tests updated/added (7 new)         │
├────────────────────────────────────────┤
│ Phase 5: Testing                       │
│ ✅ ALL unit tests: 134/134 passing     │
│ ✅ ALL integration tests: 45/45 passing│
│ ✅ Coverage: 94% (maintained)          │
│ ✅ NO Regressions detected             │
├────────────────────────────────────────┤
│ Phase 6: Documentation                 │
│ ✅ Error Log Resolution complete       │
│ ✅ Learnings documented                │
│ ✅ Prevention Strategy documented      │
│ ✅ Commit Message informative          │
└────────────────────────────────────────┘

🎉 QGD PASSED! Ready to Commit & Notify Developer

Next: Commit fix and update BACKLOG.md
```

---

## 🚨 Critical Validation Rules

**THESE RULES CANNOT BE BYPASSED:**

1. **✅ MANDATORY: ALL Tests Run**
   - Cannot proceed without running ALL tests
   - Not just affected tests
   - Must include integration tests
   - Must include coverage check

2. **✅ MANDATORY: No Regressions**
   - ALL previously passing tests must still pass
   - Coverage must not drop below 90%
   - No new failures allowed

3. **✅ MANDATORY: Root Cause Identified**
   - Cannot fix without understanding WHY
   - Symptom fix is not acceptable
   - Must document Root Cause clearly

4. **✅ MANDATORY: Resolution Documented**
   - Error Log must be updated
   - Resolution Section required
   - Learnings must be captured

5. **✅ MANDATORY: Clean Implementation**
   - No workarounds
   - No TODOs in fix
   - Clean Code Principles followed

---

## 💬 Validation Message Formats

### Success Format:

```
✅ {PHASE}

Validation successful:
  ✅ {Check 1}
  ✅ {Check 2}
  ✅ {Check 3}

Status: {Status}
Next: {Next Phase}
```

### Warning Format:

```
⚠️ {PHASE}

Quality warnings (non-blocking):
  ⚠️ {Warning 1}
  ⚠️ {Warning 2}

Recommendations:
  1. {Recommendation 1}
  2. {Recommendation 2}

Status: Acceptable but could be improved
```

### Error Format:

```
❌ {PHASE}

Validation failed ({X}/{Y} checks passed):
  ❌ {Error 1 - specific description}
  ❌ {Error 2 - specific description}

Actions required:
  1. {Concrete Action 1}
  2. {Concrete Action 2}

BLOCKED: Cannot proceed until errors fixed
```

---

## 🔄 Integration mit Developer Mode

**Automatic Validation Trigger:**

```
Developer creates Error Log
  ↓
Debugger loads Error Log
  ↓
Automatic validation:
  - Format check
  - Completeness check
  ↓
If validation fails:
  → Notify Developer
  → Request Error Log fix
  → STOP debugging

If validation passes:
  → Proceed with debugging
```

---

## 📋 Zusammenfassung

Diese Instructions stellen sicher:

✅ **Error Log Quality** - Vollständige, strukturierte Error Logs  
✅ **Root Cause Analysis** - Systematische Problem-Identifikation  
✅ **Clean Fixes** - Keine Workarounds, echte Lösungen  
✅ **Comprehensive Testing** - ALL Tests run, keine Regressions  
✅ **Documentation** - Vollständige Resolution und Learnings  
✅ **Quality Gates** - Automatic validation vor Commit  

**Ziel:** Stelle sicher, dass JEDER Fix dem Quality-Standard entspricht - systematisch, gründlich, nachhaltig!

---

**Version:** 1.0  
**Last Updated:** 2025-10-07  
**Integration:** Works with debugger.chatmode.md and developer.chatmode.md