---
applyTo: "backlog/tasks/**/*.md, src/**/*.{py,js,ts}, tests/**/*.{py,js,ts}, logs/**/*.md"
description: "Auto-validation rules for Developer Mode - enforces quality standards and test requirements"
autoLoad: true
---

# Developer - Auto-Validation Rules

> **Purpose:** These rules automatically validate quality during development. They complement the streamlined 5-phase workflow in `developer.chatmode.md`.

## 📁 Applied To

```
✅ backlog/tasks/**/*.md    → Task file structure validation
✅ src/**/*.{py,js,ts}      → Code quality validation
✅ tests/**/*.{py,js,ts}    → Test completeness validation
✅ logs/ERROR-TASK-*.md     → Error log format validation
```

---

## 🔍 Validation Rules

### Rule 1: Task File Must Be Complete (Phase 1)

**File Naming Pattern:**
```
TASK-{FEATURE-ID}-{TASK-NUM}-{slug}.md

✅ Valid: TASK-001-001-create-user-model.md
❌ Invalid: task-1-setup.md
```

**Required Sections:**
```markdown
MANDATORY:
✅ ## Description
✅ ## Technical Specification
   - Files to Create/Modify
   - Implementation Details (with code examples)
✅ ## Test Plan (unit + integration specs)
✅ ## Acceptance Criteria
✅ ## Definition of Done
✅ ## ASRs (if architecture-significant)

OPTIONAL:
○ ## Dependencies
○ ## Edge Cases
```

**Validation Error Format:**
```
❌ Task File Validation Failed

File: backlog/tasks/FEATURE-001/task-setup.md
Issues: 2

1. ❌ Invalid filename
   Found: task-setup.md
   Expected: TASK-001-XXX-setup-xyz.md

2. ❌ Missing Test Plan section
   Cannot proceed without test specifications
   
Action: Notify @architect to complete task file
```

---

### Rule 2: Code Must Meet Quality Standards (Phase 2)

**Enforced Standards:**
```python
✅ Type hints on all functions/methods
✅ Docstrings (Google/NumPy style)
✅ Input validation before processing
✅ Error handling with logging (not print())
✅ No hardcoded secrets or config
✅ No TODOs or placeholders
✅ No commented-out code

❌ Violations trigger quality check failure
```

**Quality Check Examples:**

```python
# ❌ BAD - Missing type hints, bare except, print(), TODO
def process_user(data):
    try:
        user = data['user']
        print(user)  # Debug
        # TODO: Add validation
        return user
    except:
        return None

# ✅ GOOD - Type hints, docstring, validation, logging
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

def process_user(data: Dict) -> Optional[User]:
    """Process user data from request.
    
    Args:
        data: Request data with user info
    Returns:
        User object if valid
    Raises:
        ValueError: If user data invalid
    """
    if 'user' not in data:
        logger.error("Missing 'user' key")
        raise ValueError("User data required")
    
    try:
        user = User.from_dict(data['user'])
        logger.info(f"Processed user: {user.id}")
        return user
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise
```

**Validation Error Format:**
```
⚠️ Code Quality Issues

File: src/users.py | Function: process_user
Issues: 4

1. ❌ No type hints (line 1)
   Fix: def process_user(data: Dict) -> Optional[User]:

2. ❌ Missing docstring
   Fix: Add Google/NumPy style docstring

3. ❌ Bare except clause (line 5)
   Fix: except ValidationError as e: + logging

4. ❌ print() instead of logging (line 4)
   Fix: logger.info(f"Processing user: {user.id}")

Action: Refactor per clean code principles
```

---

### Rule 3: Tests Must Be Complete (Phase 2-3)

**Required Coverage:**
```
✅ ALL test cases from Task Test Plan
✅ Minimum: 1 happy path + 1 edge case + 1 error case
✅ Descriptive test names
✅ Test docstrings
✅ Proper assertions (no empty tests)
✅ Parametrized tests for multiple scenarios

❌ NO placeholder tests ("pass" or "TODO")
❌ NO tests without assertions
❌ NO skipping test implementation
```

**Test Quality Examples:**

```python
# ❌ BAD - Placeholder, no assertions
def test_user():
    pass  # TODO

def test_user2():
    user = create_user()  # No assertion!

# ✅ GOOD - Complete tests
import pytest

class TestUserCreation:
    """User creation test suite."""
    
    def test_valid_user_creation(self):
        """Test creating user with valid data."""
        user = create_user(
            email="test@example.com",
            password="SecurePass123!"
        )
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    def test_invalid_email_raises_error(self):
        """Test error on invalid email."""
        with pytest.raises(ValidationError, match="Invalid email"):
            create_user(email="invalid", password="Pass123!")
    
    @pytest.mark.parametrize("email,password,error", [
        ("", "Pass!", "Email required"),
        ("test@ex.com", "", "Password required"),
    ])
    def test_validation_errors(self, email, password, error):
        """Test various validation scenarios."""
        with pytest.raises(ValidationError, match=error):
            create_user(email=email, password=password)
```

**Validation Error Format:**
```
❌ Test Suite Incomplete

File: tests/unit/test_users.py | Function: create_user
Issues: 3

1. ❌ Missing tests from Test Plan
   Found: 2 tests | Required: 5 tests
   Missing:
   - test_invalid_email_raises_error()
   - test_weak_password_raises_error()
   - test_validation_errors() (parametrized)

2. ❌ No edge case tests
   Add: Empty input, boundary conditions

3. ❌ Placeholder test found (line 45)
   def test_user(): pass  # TODO
   
Action: Implement ALL tests from Task Test Plan (MANDATORY)
```

---

### Rule 4: Test Execution is MANDATORY (Phase 3)

**Required Execution:**
```bash
# Use project-appropriate test commands (adapt to your stack):
# See developer.chatmode.md for complete command reference

✅ Quick check: Run affected tests
✅ Full validation: Run ALL tests with coverage (MANDATORY)
✅ Quality check: Run linter/formatter

# Supports: Python, JavaScript/TypeScript, Java, Go, C#, and more

❌ NEVER skip test execution
❌ NEVER assume tests pass
❌ NEVER commit without running tests
```

**Documentation Required:**
```
Test Results:
✅ Unit: X passed | Integration: Y passed | Coverage: Z%

OR if failed:
❌ Unit: X/Y passed (Z FAILED)
→ Error log created: logs/ERROR-TASK-XXX-YYYY-MM-DD-HHMM.md
```

**Validation Error:**
```
❌ CRITICAL: Tests Not Executed

Task: TASK-001-001-create-user-model
Status: Implementation complete ❌ Tests: NOT RUN

Action: Run canonical test suite (see chatmode)
Cannot proceed without test execution!
```

---

### Rule 5: Error Logs Required for Test Failures (Phase 3a)

**Error Log Requirements:**
```
File: logs/ERROR-TASK-XXX-YYYY-MM-DD-HHMM.md

MUST contain:
✅ Error summary (count, type, severity)
✅ Each test failure (file, error, stack trace, context)
✅ Code context (implementation + test code)
✅ Environment info (versions, dependencies)
✅ Attempted solutions

MUST trigger:
✅ STOP task execution
✅ Notify @debugger
✅ NO commit
✅ NO proceed to next task
```

---

### 5. Test Failure Handling (MANDATORY!)

**Wenn Tests fehlschlagen:**

```markdown
CHECK bei Test-Failures:

✅ Error Log erstellt?
✅ Error Log Format korrekt?
✅ Alle Failures dokumentiert?
✅ Stack Traces enthalten?
✅ Code Context enthalten?
✅ Environment Info enthalten?
✅ @debugger notified?
✅ Task execution STOPPED?

MANDATORY Error Log Creation:
File: logs/ERROR-TASK-{FEATURE}-{TASK}-{YYYY-MM-DD}-{HHMM}.md

VERBOTEN:
❌ Test-Failures ignorieren
❌ "Will fix later"
❌ Commit trotz failing tests
❌ Continue to next task
❌ Mark task as complete
```

**Error Log Template Required:**

```markdown
# Error Log: TASK-XXX-YYY

**Task ID:** TASK-XXX-YYY  
**Task Title:** [Title]  
**Date:** YYYY-MM-DD HH:MM  
**Developer:** Developer Mode  
**Status:** ❌ Tests Failed  

## Error Summary
**Failed Tests:** X out of Y tests failed  
**Test Type:** Unit | Integration | Both  
**Severity:** High | Medium | Low

## Test Failures
[Detaillierte Test-Failure-Info]

## Code Context
[Relevanter Code]

## Environment Information
[Environment Details]

## Attempted Solutions
[Was wurde versucht]

## Next Steps for @debugger
[Was Debugger analysieren soll]
```

**Fehlermeldung bei fehlender Error Log Creation:**

```
❌ CRITICAL: Error Log nicht erstellt!

Test Results:
❌ Unit Tests: 12/15 passed, 3 FAILED
❌ Integration Tests: 5/8 passed, 3 FAILED

MANDATORY Action:
  Wenn Tests fehlschlagen, MUSS Error Log erstellt werden!

Action erforderlich:
  1. Erstelle: logs/ERROR-TASK-001-001-2025-10-07-1430.md
  2. Dokumentiere ALLE Test Failures
  3. Include Stack Traces
  4. Include Code Context
  5. Include Environment Info
  6. Notify @debugger
  7. STOP Task Execution

Template: .github/templates/ERROR-LOG-TEMPLATE.md

UNTIL Error Log created, task is BLOCKED!
```

---

### 6. Acceptance Criteria Validation

**Vor Marking Task Complete:**

```markdown
CHECK Acceptance Criteria:

✅ Alle Criteria aus Task erfüllt?
✅ Functionality wie spezifiziert?
✅ Edge Cases behandelt?
✅ Performance akzeptabel?
✅ Keine Regressionen?

ALLE Criteria müssen ✅ sein:
- [ ] Criterion 1 aus Task
- [ ] Criterion 2 aus Task
- [ ] Criterion 3 aus Task
- [ ] ALL Tests passed
- [ ] Coverage >90%

VERBOTEN:
❌ "Mostly works"
❌ "Good enough"
❌ Unerfüllte Criteria ignorieren
```

**Fehlermeldung bei unerfüllten Criteria:**

```
⚠️ Acceptance Criteria nicht erfüllt

Task: TASK-001-001-create-user-model
Status: Implementation complete
Acceptance Criteria: 3/5 ✅

Erfüllte Criteria:
  ✅ User model has all required fields
  ✅ Email field has unique constraint
  ✅ Migration runs successfully

Nicht erfüllte Criteria:
  ❌ Timestamps auto-update
     → created_at/updated_at nicht automatisch
  ❌ All tests pass
     → 2 Tests failing

Action erforderlich:
  Fix unerfüllte Criteria:
  
  1. Timestamps auto-update:
     Add server_default=func.now() and onupdate=func.now()
  
  2. Fix failing tests:
     Run tests und behebe Failures

Task kann NICHT als complete markiert werden bis
ALLE Acceptance Criteria erfüllt sind!
```

---

### 7. Definition of Done Validation

**Final Check vor Commit:**

```markdown
CHECK Definition of Done:

✅ Code implemented as specified?
✅ Unit tests written and passing?
✅ Integration tests written and passing?
✅ Code reviewed (self-review)?
✅ Documentation updated?
✅ No TODOs oder Platzhalter?
✅ Clean Code Principles befolgt?
✅ BACKLOG.md Code-Mapping bereit?

ALLE Items müssen ✅ sein!

VERBOTEN:
❌ "Almost done"
❌ Skip DoD Items
❌ "Will do later"
```

**Validation Error:**
```
❌ Definition of Done Incomplete

Task: TASK-001-001 | DoD: 5/7 ✅

Complete:
✅ Code implemented
✅ Tests passing
✅ Self-reviewed
✅ No TODOs

Incomplete:
❌ Documentation not updated
❌ BACKLOG.md not updated

Action: Complete DoD items before commit
```

---

### Rule 6: Commit Message Must Be Informative (Phase 4)

**Required Format:**
```
type(scope): TASK-XXX - Brief description

Implementation:
- Change 1
- Change 2

Testing:
- Unit: X passed | Integration: Y passed | Coverage: Z%

Closes TASK-XXX | Refs FEATURE-XXX
```

**Examples:**
```
❌ BAD: "added user model"
   (no type, scope, task ref, testing info)

✅ GOOD: feat(models): TASK-001-001 - User database model

Implementation:
- User model with email, password fields
- Unique email constraint
- Auto timestamps

Testing:
- Unit: 15 passed | Integration: 8 passed | Coverage: 94%

Closes TASK-001-001 | Refs FEATURE-001
```

---

## 🎯 Non-Bypassable Rules

### Rule Alpha: NO Code Without Tests
```
❌ NEVER write code without tests
❌ NEVER commit untested code
❌ NEVER "add tests later"

✅ ALWAYS write tests during implementation
✅ ALWAYS run tests before commit
```

### Rule Beta: NO Commit Without Passing Tests
```
❌ NEVER commit with failing tests
❌ NEVER skip test execution
❌ NEVER mock test results

✅ ALL tests MUST pass OR error log created
✅ Coverage ≥90% maintained
✅ @debugger notified if failures
```

### Rule Gamma: NO Task Complete Without Full Test Suite
```
❌ NEVER mark task complete without tests
❌ NEVER skip Test Plan implementation
❌ NEVER incomplete test coverage

✅ ALL Test Plan tests implemented
✅ ALL tests executed
✅ ALL tests passing OR error log + @debugger
```

---

### 8. Commit Message Validation

**Commit Message Quality Check:**

```markdown
CHECK Commit Message:

✅ Type correct? (feat|fix|test|docs|refactor|chore)
✅ Scope present?
✅ Brief description clear?
✅ Implementation section vorhanden?
✅ Testing section vorhanden?
✅ Test results dokumentiert?
✅ References Task?
✅ References Feature/Issue?

Format:
type(scope): TASK-XXX-YYY - Brief description

Implementation:
- Change 1
- Change 2

Testing:
- Unit tests: X passing
- Integration tests: Y passing
- Coverage: Z%

Closes TASK-XXX-YYY
References FEATURE-XXX, ISSUE-XXX
```

**Beispiel - BAD Commit:**

```
❌ BAD:
"added user model"

Problems:
1. No type
2. No scope
3. No task reference
4. No testing info
```

**Beispiel - GOOD Commit:**

```
✅ GOOD:
feat(models): TASK-001-001 - create User database model

Implementation:
- Created User model with email, password_hash fields
- Added unique constraint on email
- Added automatic timestamps (created_at, updated_at)
- Created Alembic migration for users table

Testing:
- Unit tests: 15/15 passing
- Integration tests: 8/8 passing
- Coverage: 94%

Closes TASK-001-001
References FEATURE-001, ISSUE-001
```

**Fehlermeldung bei schlechter Commit Message:**

```
⚠️ Commit Message unzureichend

Gefunden: "added user model"

Probleme:
1. ❌ Kein Type (feat|fix|...)
2. ❌ Kein Scope (models)
3. ❌ Kein Task Reference
4. ❌ Keine Implementation Details
5. ❌ Keine Testing Information
6. ❌ Keine References

Action erforderlich:
  Schreibe informative Commit Message mit:
  - Type und Scope
  - Task Reference
  - Implementation Details
  - Testing Results
  - References zu Feature/Issue

Template: .github/templates/COMMIT-MESSAGE-TEMPLATE.txt
```

---

## 🎯 Test-Enforcement Rules (CANNOT BE BYPASSED)

**Diese Regeln sind NICHT optional:**

### Rule 1: No Code Without Tests

```
❌ NICHT ERLAUBT:
- Code schreiben ohne Tests
- Tests "später" schreiben
- Tests überspringen

✅ MANDATORY:
- Tests schreiben (Phase 4)
- Tests ausführen (Phase 5)
- Tests passing (Phase 5)
```

### Rule 2: ALL Tests Must Pass

```
❌ NICHT ERLAUBT:
- Commit mit failing tests
- "Most tests pass"
- Failing tests ignorieren

✅ MANDATORY:
- 100% Tests passing
- Error Log if failures
- @debugger notification
```

### Rule 3: Comprehensive Testing Required

```
❌ NICHT ERLAUBT:
- Nur affected tests run
- Skip integration tests
- "Assume tests pass"

✅ MANDATORY:
- ALL unit tests run
- ALL integration tests run
- Coverage check performed
```

### Rule 4: Error Logs for Failures

```
❌ NICHT ERLAUBT:
- Continue without Error Log
- Skip Error Log creation
- "Will fix myself"

✅ MANDATORY:
- Create Error Log immediately
- Document all failures
- Notify @debugger
- STOP task execution
```

### Rule 5: Coverage Maintained

```
❌ NICHT ERLAUBT:
- Coverage drop below 90%
- "Coverage doesn't matter"
- Skip coverage check

✅ MANDATORY:
- Maintain >90% coverage
- New code 100% coverage
- Coverage check in tests
```

---

---

## 🎯 Quality Gates (Streamlined)

**Pre-Commit Validation:**

```
Phase 1: Task Analysis & Setup
  ✅ Task file valid + Test Plan present
  ✅ Dependencies ready + ASRs understood

Phase 2: Implementation
  ✅ Code follows spec + Clean code applied
  ✅ Tests written + No TODOs

Phase 3: Testing & Validation
  ✅ ALL tests executed + ALL passing
  ✅ Coverage ≥90% + No regressions

Phase 4: Validation & Commit
  ✅ Acceptance criteria met + DoD complete
  ✅ Commit message informative

Phase 5: Completion & Metrics
  ✅ BACKLOG.md updated + Metrics tracked

ALL ✅ → Commit allowed
ANY ❌ → BLOCK + Show specific failure
```

---

## 🚨 Critical Blocks (Cannot Proceed)

```
❌ Tests not written
   → Write ALL tests from Test Plan (MANDATORY)

❌ Tests not executed
   → Run canonical test suite (MANDATORY)

❌ Tests failing
   → Create Error Log → Notify @debugger → STOP

❌ Coverage <90%
   → Add tests to increase coverage

❌ Error log missing (when tests fail)
   → Create complete error log (MANDATORY)
```

---

## 💬 Validation Messages

**Success:**
```
✅ {Phase Name}
Status: Ready for next phase
```

**Block:**
```
❌ CRITICAL: {Phase} BLOCKED
Issue: {Description}
Action: {Required steps}
Cannot proceed until resolved
```

**Warning:**
```
⚠️ {Phase Name}
Issue: {Description}
Recommendation: {Suggestion}
Can proceed but not recommended
```

---

## 📊 Metrics & Continuous Improvement

**Track:**
- Task duration (start to commit)
- Test pass rate (first attempt %)
- Error log frequency
- Coverage trends
- Code quality scores

**Learn:**
- Analyze error patterns
- Identify common failures
- Suggest architectural improvements
- Optimize process

---

## 📌 Summary

**Purpose:** Auto-validate quality during development

**Key Principles:**
1. ✅ Quality over speed
2. ✅ Testing is MANDATORY
3. ✅ Clean code enforced
4. ✅ Systematic error handling
5. ✅ Continuous improvement

**Core Rule:** **"No Code Ships Without Tests"**

---

**Version:** 4.0 (Streamlined Validation)  
**Last Updated:** 2025-11-02  
**Integration:** Works with developer.chatmode.md (5-Phase Workflow)

---

## 🚨 Critical Validation Failures

**INSTANT BLOCKS (Cannot Proceed):**

1. **❌ Tests Not Written**
   ```
   BLOCK: Cannot proceed past Phase 4 without tests
   REASON: Test-Driven Development is MANDATORY
   ACTION: Write ALL tests from Test Plan
   ```

2. **❌ Tests Not Executed**
   ```
   BLOCK: Cannot mark task complete without test execution
   REASON: Test execution is MANDATORY
   ACTION: Run ALL tests (unit + integration + coverage)
   ```

3. **❌ Tests Failing**
   ```
   BLOCK: Cannot commit with failing tests
   REASON: Only passing tests can be committed
   ACTION: Create Error Log → Notify @debugger → STOP
   ```

4. **❌ Coverage Below 90%**
   ```
   BLOCK: Cannot proceed with insufficient coverage
   REASON: >90% coverage is MANDATORY
   ACTION: Add tests to increase coverage
   ```

5. **❌ Error Log Not Created (when tests fail)**
   ```
   BLOCK: Cannot continue without Error Log
   REASON: Debugging requires documentation
   ACTION: Create complete Error Log → Notify @debugger
   ```

---

## 💬 Validation Message Formats

### Success Format:

```
✅ {PHASE}

Validation successful:
  ✅ {Check 1}
  ✅ {Check 2}

Status: Ready for {Next Phase}
```

### Critical Block Format:

```
❌ CRITICAL: {PHASE} BLOCKED

Blocking Issue:
  ❌ {Issue Description}

Impact: {Impact Description}

Action Required:
  1. {Specific Action 1}
  2. {Specific Action 2}

CANNOT PROCEED until resolved!
```

---

## 🔄 Integration Points

### Mit Architect:

```
Architect erstellt Task
  ↓
Includes Test Plan (MANDATORY)
  ↓
Developer reads Task
  ↓
Validates Test Plan presence
  ↓
If missing → Notify @architect
```

### Mit Debugger:

```
Developer runs tests
  ↓
Tests fail ❌
  ↓
Create Error Log (MANDATORY)
  ↓
Notify @debugger
  ↓
STOP task execution
  ↓
Wait for @debugger fix
```

---

## 📋 Zusammenfassung

Diese Instructions stellen sicher:

✅ **Test-First Approach** - Tests sind MANDATORY, nicht optional  
✅ **Quality Enforcement** - Clean Code + Type Hints + Validation  
✅ **Comprehensive Testing** - ALL Tests run, >90% Coverage  
✅ **Error Handling** - Error Logs bei Test-Failures  
✅ **Documentation** - Code, Tests, Commits vollständig dokumentiert  
✅ **No Shortcuts** - Kein Code shipped ohne Tests  

**Ziel:** Stelle sicher, dass JEDER Task dem Quality-Standard entspricht - mit MANDATORY Testing als Fundament!

---

**Version:** 1.0  
**Last Updated:** 2025-10-07  
**Critical Feature:** Test-Enforcement (MANDATORY)  
**Integration:** Works with developer.chatmode.md and debugger.chatmode.md