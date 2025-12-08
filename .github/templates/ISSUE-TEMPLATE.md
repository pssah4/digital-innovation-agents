# ISSUE-XXX: [Action-Oriented Title - What to Build]

> **Feature:** [FEATURE-XXX](../features/FEATURE-XXX-*.md) - [Feature Name]  
> **ID:** ISSUE-XXX  
> **Type:** Feature | Bug Fix | Refactor | Test | Documentation  
> **Priority:** P0-Critical | P1-High | P2-Medium | P3-Low  
> **Effort:** Tiny (2-4h) | Small (4-8h) | Medium (1-2d) | Large (2-3d)  
> **Status:** 📋 Ready | 🔵 In Progress | ✅ Done | ❌ Blocked  
> **Sprint:** Sprint X | Backlog  
> **Created:** YYYY-MM-DD  

---

> ⚠️ **ATOMIC ISSUE PRINCIPLE:** Dieses Issue muss in 1-3 Tagen abschließbar sein!  
> Falls >3 Tage geschätzt → Issue muss aufgeteilt werden.

---

## 📝 Context

[1-2 Absätze: Warum existiert dieses Issue? Welches Problem löst es? Business Context.]

**Contribution to Feature:**  
[Wie ermöglicht dieses Issue das Parent Feature?]

**User Impact:**  
[Wie werden End-User diese Funktionalität erleben?]

---

## 🏗️ Architectural Context

**Related ADRs:**
- [ADR-XXX](../../architecture/ADR-XXX-*.md) - [Decision Title]
- [ADR-YYY](../../architecture/ADR-YYY-*.md) - [Decision Title]

**arc42 Reference:**  
Section [X.X] - [Section Name]

**Architectural Decision Summary:**  
> Wir haben uns für [Entscheidung] entschieden, weil [Rationale aus ADR].  
> Dies bedeutet für dieses Issue: [Implikation].

**Component:**  
[Welche architektonische Komponente betrifft dieses Issue?]

**System Context:**
```
[Einfaches Diagramm oder Beschreibung wo dieses Issue im System liegt]

[Component A] → [DIESES ISSUE] → [Component B]
                      ↓
               [External API]
```

---

## 📋 Requirements

### Functional Requirements

**Was gebaut werden muss:**

1. [Spezifische Anforderung 1]
2. [Spezifische Anforderung 2]
3. [Spezifische Anforderung 3]

**Beispiel (falls hilfreich):**
```python
# Erwartete Struktur/Pattern (NICHT vollständige Implementation!)
class UserModel:
    email: str
    password_hash: str
    created_at: datetime
```

### Non-Functional Requirements

**Performance (falls relevant):**
- [Requirement mit konkretem Wert]

**Security (falls relevant):**
- [Requirement mit konkretem Standard]

---

## 🎯 Acceptance Criteria

> ⚠️ **Jedes Kriterium muss eindeutig testbar sein!**

**Dieses Issue ist fertig wenn:**

- [ ] **AC1:** [Spezifisch und testbar]
  - Verification: [Wie wird das verifiziert?]
  
- [ ] **AC2:** [Spezifisch und testbar]
  - Verification: [Wie wird das verifiziert?]
  
- [ ] **AC3:** [Spezifisch und testbar]
  - Verification: [Wie wird das verifiziert?]

**Gherkin Scenarios (aus Feature):**
- [Scenario aus FEATURE-XXX](../features/FEATURE-XXX-*.md#scenario-1)

---

## 🔧 Implementation Guidance

> ℹ️ **High-Level Guidance, NICHT Step-by-Step!** Developer entscheidet über Details.

**Files to Create/Modify:**
```
src/models/user.py      # Create
src/services/auth.py    # Modify
tests/test_user.py      # Create
docs/api/users.md       # Update
```

**Suggested Approach:**
1. [High-Level Schritt - z.B. "Define User model mit SQLAlchemy"]
2. [High-Level Schritt - z.B. "Add validation methods"]
3. [High-Level Schritt - z.B. "Create database migration"]

**Key Patterns/Standards:**
- Follow [Pattern aus ADR-XXX]
- Use [Library] for [Purpose]
- Reference [Example in Codebase]

---

## 🔒 Architectural Constraints (Non-Negotiable!)

> ⚠️ **MUST/MUST NOT - Diese Constraints sind nicht verhandelbar!**

**MUST:**
- [Constraint 1 - z.B. "Use bcrypt for password hashing (ADR-XXX)"]
- [Constraint 2 - z.B. "Follow RESTful conventions"]
- [Constraint 3 - z.B. "All endpoints require authentication"]

**MUST NOT:**
- [Anti-Pattern 1 - z.B. "Store passwords in plain text"]
- [Anti-Pattern 2 - z.B. "Use synchronous calls to external APIs"]
- [Anti-Pattern 3 - z.B. "Hardcode configuration values"]

**Performance Constraints (falls kritisch):**
- [z.B. "Query must complete in <100ms"]

**Security Constraints (falls kritisch):**
- [z.B. "All user input must be sanitized"]

---

## 🔓 Open for Developer Decision

> ✅ **Developer hat volle Autonomie über diese Aspekte:**

- **Internal Code Structure:** [z.B. "How to organize helper functions"]
- **Variable/Method Naming:** [Developer's choice within style guide]
- **Algorithm Choice:** [z.B. "Choice of sorting algorithm" - unless constrained]
- **Library Selection:** [z.B. "Choice of validation library within stack"]
- **Error Message Wording:** [Developer's choice]
- **Logging Details:** [What/how much to log]
- **Test Organization:** [How to structure test files]

---

## 🧪 Testing Requirements

> ⚠️ **MANDATORY - Issue ist nicht Done ohne Tests!**

### Unit Tests (PFLICHT)

- [ ] Test happy path scenario
- [ ] Test error handling (invalid input)
- [ ] Test edge cases: [spezifische Edge Cases]
- [ ] Test validation logic
- [ ] Test error messages

**Minimum Coverage:** 80% für neuen Code

### Integration Tests (falls relevant)

- [ ] Test [Integration Scenario 1]
- [ ] Test [Integration Scenario 2]
- [ ] Test database interactions
- [ ] Test API responses

### Performance Tests (falls NFR definiert)

- [ ] Response time < [X]ms
- [ ] Can handle [X] concurrent requests

---

## ✅ Definition of Done

**Code:**
- [ ] Code implementiert wie spezifiziert
- [ ] Alle Acceptance Criteria erfüllt
- [ ] Alle Architectural Constraints eingehalten
- [ ] Code follows Style Guide
- [ ] Keine Linting Errors

**Tests:**
- [ ] Unit Tests geschrieben und bestanden
- [ ] Integration Tests bestanden (falls relevant)
- [ ] Coverage > 80% für neuen Code

**Quality:**
- [ ] Self-Review durchgeführt
- [ ] Code Review bestanden
- [ ] Keine bekannten Bugs

**Documentation:**
- [ ] Inline Comments wo nötig
- [ ] API Documentation aktualisiert (falls API geändert)
- [ ] README aktualisiert (falls nötig)

**Deployment:**
- [ ] Committed mit klarer Message
- [ ] CI/CD Pipeline passed
- [ ] Deployed to Staging (falls relevant)

---

## 🔗 Dependencies

**Blocked By (Muss zuerst fertig sein):**
- [ISSUE-XXX](./ISSUE-XXX-*.md) - [Warum blockiert]

**Blocks (Wartet auf dieses Issue):**
- [ISSUE-YYY](./ISSUE-YYY-*.md) - [Was wird ermöglicht]

**Related (Keine Blockade, aber relevant):**
- [ISSUE-ZZZ](./ISSUE-ZZZ-*.md) - [Wie sie zusammenhängen]

---

## 💡 Notes for Developer

**Helpful Context:**
[Zusätzlicher Kontext, Gotchas, oder Implementation Tips]

**Common Pitfalls:**
- [Pitfall 1 zu vermeiden]
- [Pitfall 2 zu vermeiden]

**Helpful Resources:**
- [Documentation Link]
- [Example in Codebase]
- [Stack Overflow / Blog Post]

---

## 📚 References

**Architecture:**
- ADR: [Link zu relevantem ADR]
- arc42: [Link zu relevantem Section]

**Requirements:**
- Feature: [Link zu FEATURE-XXX]
- Gherkin Scenarios: [Link]

**Technical:**
- [Framework Documentation]
- [API Reference]

---

## 📝 Change Log

| Datum | Änderung | Autor |
|-------|----------|-------|
| YYYY-MM-DD | Issue erstellt | Architect |

---

**Template Version:** 2.0  
**Workflow:** RE (Feature) → Architect (erstellt Issue) → Developer (implementiert)  
**Erstellt von:** Architect  
**Atomic Principle:** Max 1-3 Tage Effort!
