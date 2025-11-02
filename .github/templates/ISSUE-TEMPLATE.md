# ISSUE-XXX: [Issue Title]

> **Epic:** [EPIC-XXX](../epics/EPIC-XXX-epic-name.md) - [Epic Name]  
> **Feature:** [FEATURE-XXX](../features/FEATURE-XXX-feature-name.md) - [Feature Name]  
> **ID:** ISSUE-XXX  
> **Story Points:** X (Fibonacci: 1,2,3,5,8,13)  
> **Priority:** P0-Critical | P1-High | P2-Medium | P3-Low  
> **Status:** 📋 Not Started | 🚧 In Progress | ✅ Done | 🔄 In Review  
> **Owner:** [Developer Name]  
> **Sprint:** Sprint X | Backlog  

---

## 📝 Business Context

**Why This Issue Matters:**
[Explain how this issue contributes to the feature's business value]

**Contribution to Feature:**
[Specific capability this issue enables within the parent feature]

**User Impact:**
[How end-users will experience this functionality]

---

## 📖 User Story

**As a** [specific user persona]  
**I want to** [specific capability]  
**So that** [specific benefit/value]

**Example Scenario:**
[Concrete example of user using this functionality]

---

## ✅ Acceptance Criteria

**This issue is complete when:**

1. **Criterion 1:** [Specific, testable requirement]
   - Measurement: [How we verify it]
   - Pass Condition: [What success looks like]

2. **Criterion 2:** [Specific, testable requirement]
   - Measurement: [How we verify it]
   - Pass Condition: [What success looks like]

3. **Criterion 3:** [Specific, testable requirement]
   - Measurement: [How we verify it]
   - Pass Condition: [What success looks like]

4. **Criterion 4:** [Specific, testable requirement]
   - Measurement: [How we verify it]
   - Pass Condition: [What success looks like]

5. **Criterion 5:** [Specific, testable requirement]
   - Measurement: [How we verify it]
   - Pass Condition: [What success looks like]

---

## 🥒 Gherkin Scenarios

### Scenario 1: [Happy Path - Successful Case]

```gherkin
Feature: [Feature Name from FEATURE-XXX]

Scenario: [Descriptive scenario name with specific conditions]
  Given a registered user with email "user@example.com"
  And the user has password "SecurePass123!"
  And the user is on the login page at "/login"
  And the user's account is active and verified
  When the user enters email "user@example.com" into the email field
  And the user enters password "SecurePass123!" into the password field
  And the user clicks the "Login" button
  Then the user is redirected to the dashboard at "/dashboard"
  And a welcome message "Welcome back, User!" is displayed in the header
  And a session token is created with 24-hour expiry
  And the user's last login timestamp is updated to current time
  And the user sees their personalized dashboard widgets
```

### Scenario 2: [Error/Edge Case - Failure Case]

```gherkin
Scenario: [Descriptive scenario name for error condition]
  Given a registered user with email "user@example.com"
  And the user has password "SecurePass123!"
  And the user is on the login page at "/login"
  And the user's account has been locked after 5 failed attempts
  When the user enters email "user@example.com" into the email field
  And the user enters password "SecurePass123!" into the password field
  And the user clicks the "Login" button
  Then the user remains on the login page at "/login"
  And an error message is displayed: "Account locked due to multiple failed login attempts"
  And the error message includes text "Please contact support or wait 30 minutes"
  And no session token is created
  And no redirect occurs
  And the login form is disabled for 30 minutes
  And an email is sent to "user@example.com" about the locked account
```

### Scenario 3: [Additional Edge Case - Optional but Recommended]

```gherkin
Scenario: [Another important edge case or variation]
  Given [specific preconditions with concrete values]
  And [additional context]
  When [specific user action with concrete values]
  And [additional actions if needed]
  Then [specific expected outcome with concrete values]
  And [additional expected results]
  And [state changes or side effects]
```

---

## 🔧 Technical Notes

**Implementation Approach:**
[High-level technical approach, but NOT detailed implementation]

**Components Involved:**
- [Component 1]: [Responsibility]
- [Component 2]: [Responsibility]
- [Component 3]: [Responsibility]

**Data Models:**
- [Entity 1]: [Fields needed]
- [Entity 2]: [Fields needed]

**APIs/Endpoints:**
- [Endpoint 1]: [Method, Purpose]
- [Endpoint 2]: [Method, Purpose]

**Technology Constraints:**
- [Framework/Library]: [Version, requirement]
- [Database]: [Schema changes needed]
- [External Service]: [Integration point]

---

## 🔀 Dependencies

**Blocked By (Must complete first):**
- [ISSUE-XXX](./ISSUE-XXX-issue-name.md) - [Why this blocks us]
- [External Dependency] - [What we need]

**Blocks (This must be done before):**
- [ISSUE-XXX](./ISSUE-XXX-issue-name.md) - [What this enables]

**Related Issues:**
- [ISSUE-XXX](./ISSUE-XXX-issue-name.md) - [How they relate]

---

## 🚨 Edge Cases

**Edge Case 1: [Scenario Name]**
- **Description:** [What makes this an edge case]
- **Trigger:** [Specific condition that causes it]
- **Expected Behavior:** [How system should respond]
- **Covered in Scenario:** [Which Gherkin scenario covers this]

**Edge Case 2: [Scenario Name]**
- **Description:** [What makes this an edge case]
- **Trigger:** [Specific condition that causes it]
- **Expected Behavior:** [How system should respond]
- **Covered in Scenario:** [Which Gherkin scenario covers this]

**Edge Case 3: [Scenario Name]**
- **Description:** [What makes this an edge case]
- **Trigger:** [Specific condition that causes it]
- **Expected Behavior:** [How system should respond]
- **Covered in Scenario:** [Which Gherkin scenario covers this]

---

## 🚫 Out of Scope

**NOT included in this issue:**

1. **[Feature/Behavior]** - [Reason] - [Where it will be handled]
2. **[Feature/Behavior]** - [Reason] - [Where it will be handled]
3. **[Feature/Behavior]** - [Reason] - [Where it will be handled]

---

## 🧪 Testing Requirements

**Unit Tests Required:**
- [ ] Test happy path scenario
- [ ] Test error handling (invalid input)
- [ ] Test edge cases (null, empty, boundary values)
- [ ] Test validation logic
- [ ] Test error messages
- [ ] Test state changes
- [ ] Minimum 90% code coverage

**Integration Tests Required:**
- [ ] Test full workflow end-to-end
- [ ] Test database interactions
- [ ] Test API responses
- [ ] Test external service integrations
- [ ] Test authentication/authorization
- [ ] Test concurrent operations
- [ ] Test rollback scenarios

**Performance Tests:**
- [ ] Response time < [X]ms for 95th percentile
- [ ] Can handle [X] concurrent requests
- [ ] Memory usage stays below [X]MB

**Security Tests:**
- [ ] Input validation prevents injection
- [ ] Authorization checks enforced
- [ ] Sensitive data encrypted/masked
- [ ] Rate limiting works correctly

---

## 📊 Definition of Done

**Technical Completion:**
- [ ] All acceptance criteria met
- [ ] All Gherkin scenarios pass
- [ ] Unit tests written and passing (≥90% coverage)
- [ ] Integration tests written and passing
- [ ] Performance requirements met
- [ ] Security requirements met
- [ ] Code follows style guidelines
- [ ] No code smells or technical debt
- [ ] Error handling implemented
- [ ] Logging implemented
- [ ] No hardcoded values (use config)

**Documentation:**
- [ ] Inline code comments added
- [ ] API documentation updated
- [ ] README updated (if needed)
- [ ] Architectural docs updated (if significant change)

**Quality Assurance:**
- [ ] Code reviewed and approved
- [ ] Manual testing completed
- [ ] Exploratory testing completed
- [ ] Edge cases validated
- [ ] Error scenarios validated

**Deployment:**
- [ ] Database migrations created (if needed)
- [ ] Configuration changes documented
- [ ] Environment variables defined
- [ ] Deployment script updated (if needed)
- [ ] Rollback plan documented

---

## 📚 References

**Related Documents:**
- [Epic](../epics/EPIC-XXX-epic-name.md)
- [Feature](../features/FEATURE-XXX-feature-name.md)
- [Technical Specs]
- [Design Docs]

**External Resources:**
- [API Documentation]
- [Framework Docs]
- [Industry Standards]

---

## 💡 Implementation Hints

**Suggested Approach:**
[High-level guidance on how to approach this, but not prescriptive implementation details]

**Common Pitfalls:**
[Known issues or mistakes to avoid]

**Testing Tips:**
[Suggestions for effective testing]

---

## 📝 Notes

[Any additional context, considerations, or information]

---

**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD  
**Reviewed By:** [Name]  
**Approved By:** [Name]
