# BUGFIX-XXX: [Bug Title]

> **Original Issue:** [ISSUE-XXX](../issues/ISSUE-XXX-issue-name.md) - [Original Issue Name]  
> **Bug ID:** BUGFIX-XXX  
> **Severity:** Critical | High | Medium | Low  
> **Architecture Impact:** None | Low | Medium | High  
> **Priority:** P0-Critical | P1-High | P2-Medium | P3-Low  
> **Status:** 📋 Not Started | 🚧 In Progress | ✅ Done | 🔄 In Review  
> **Reported By:** [Name/Email]  
> **Assigned To:** [Developer Name]  
> **Sprint:** Sprint X | Hotfix  

---

## 🐛 Bug Description

**Summary:**
[Clear, concise description of the bug]

**Environment:**
- **Version:** [Software version where bug occurs]
- **Platform:** [OS, Browser, Device]
- **Configuration:** [Relevant config settings]
- **Data State:** [Specific data conditions]

**Affected Users:**
- **Number:** [How many users affected]
- **Segments:** [Which user types/segments]
- **Impact:** [How it impacts them]

**Discovery:**
- **Found By:** [User report, monitoring, testing]
- **Date Discovered:** YYYY-MM-DD
- **Frequency:** Always | Often | Sometimes | Rarely

---

## 🔍 Steps to Reproduce

**Preconditions:**
- [Required system state]
- [Required data setup]
- [Required user permissions]
- [Required configuration]

**Reproduction Steps:**

1. **Step 1:** [Specific action with concrete values]
   - Navigate to: `[URL/Page]`
   - Ensure: [Precondition]

2. **Step 2:** [Specific action with concrete values]
   - Click: [Specific element]
   - Enter: "[Specific value]"

3. **Step 3:** [Specific action with concrete values]
   - Observe: [What happens]
   - Check: [What to verify]

4. **Step 4:** [Final action that triggers bug]
   - Action: [Specific trigger]
   - Result: [Bug manifests]

**Reproduction Rate:**
- [ ] 100% (Always reproducible)
- [ ] 75-99% (Highly reproducible)
- [ ] 50-74% (Often reproducible)
- [ ] 25-49% (Sometimes reproducible)
- [ ] <25% (Rarely reproducible)

**Screenshots/Videos:**
[Attach or link to visual evidence]

---

## ✅ Expected Behavior

**What SHOULD happen:**
[Detailed description of correct behavior]

**Correct Workflow:**
1. [Step 1] → [Expected result]
2. [Step 2] → [Expected result]
3. [Step 3] → [Expected result]

**Expected Output:**
```
[Example of correct output/response/state]
```

**Specifications Reference:**
- **Requirements:** [Link to ISSUE-XXX]
- **Design Specs:** [Link to design docs]
- **API Docs:** [Link to API documentation]

---

## ❌ Actual Behavior

**What ACTUALLY happens:**
[Detailed description of incorrect behavior]

**Broken Workflow:**
1. [Step 1] → [Actual result]
2. [Step 2] → [Actual result]
3. [Step 3] → [Problem occurs]

**Actual Output:**
```
[Example of incorrect output/response/state]
```

**Error Messages:**
```
[Exact error message if applicable]
```

**System Logs:**
```
[Relevant log entries]
```

**Stack Trace:**
```
[Full stack trace if available]
```

---

## 🔎 Root Cause Analysis

**Investigation Process:**
[How the bug was investigated]

**Root Cause:**
[Specific technical reason for the bug]

**Code Location:**
- **File:** `[file path]`
- **Lines:** [XXX-YYY]
- **Component:** [Component name]
- **Function/Method:** `[method name]`

**Problematic Code:**
```[language]
// Current (buggy) implementation
[Show the code causing the issue]
```

**Why It Fails:**
[Detailed technical explanation of why the code fails]

**Contributing Factors:**
1. **Factor 1:** [What contributed to the bug]
2. **Factor 2:** [What contributed to the bug]
3. **Factor 3:** [What contributed to the bug]

**When It Was Introduced:**
- **Commit:** [Commit hash if known]
- **Date:** YYYY-MM-DD
- **PR/Issue:** [Link to original change]
- **Why It Wasn't Caught:** [Why tests didn't catch it]

---

## 🔧 Proposed Fix

**Solution Approach:**
[High-level description of the fix]

**Fixed Code:**
```[language]
// Proposed (fixed) implementation
[Show the corrected code]
```

**Changes Required:**
- **Files to Modify:** 
  - `[file path 1]` (lines XXX-YYY)
  - `[file path 2]` (lines XXX-YYY)
  
- **New Files:** [If any]
- **Files to Delete:** [If any]

**Why This Fixes It:**
[Detailed explanation of how the fix addresses the root cause]

**Alternative Solutions Considered:**
1. **Alternative 1:** [Description] - [Why not chosen]
2. **Alternative 2:** [Description] - [Why not chosen]

---

## 🧪 Test Scenarios

### Test Scenario 1: Verify Fix (Reproduction Steps)

```gherkin
Feature: [Feature Name]

Scenario: Bug is fixed - original reproduction steps now work correctly
  Given [preconditions from reproduction steps]
  And [specific state that caused the bug]
  When [perform step 1 from reproduction]
  And [perform step 2 from reproduction]
  And [perform step 3 from reproduction]
  Then [expected behavior occurs instead of bug]
  And [verify all expected outcomes]
  And [system state is correct]
  And [no error messages appear]
```

### Test Scenario 2: Regression Prevention

```gherkin
Scenario: Fix does not break related functionality
  Given [preconditions for related functionality]
  When [perform related operations]
  Then [related functionality still works correctly]
  And [no new bugs introduced]
  And [existing features unaffected]
```

### Test Scenario 3: Edge Cases

```gherkin
Scenario: Fix handles edge cases correctly
  Given [edge case conditions]
  When [perform actions that previously failed]
  Then [system handles edge cases gracefully]
  And [appropriate behavior in all edge cases]
  And [no unexpected errors]
```

---

## 🔄 Regression Risk

**Risk Level:** None | Low | Medium | High | Critical

**Areas at Risk:**
1. **[Component/Feature 1]** - [Why at risk] - [Mitigation]
2. **[Component/Feature 2]** - [Why at risk] - [Mitigation]
3. **[Component/Feature 3]** - [Why at risk] - [Mitigation]

**Regression Test Plan:**
- [ ] Run all existing unit tests
- [ ] Run all existing integration tests
- [ ] Run E2E tests for affected workflows
- [ ] Manual testing of related features
- [ ] Performance testing (if applicable)
- [ ] Security testing (if security-related)

**Monitoring After Deployment:**
- [ ] Monitor error rates for 24h
- [ ] Monitor performance metrics
- [ ] Monitor user reports
- [ ] Set up alerts for related issues

---

## 🔀 Dependencies

**Blocks:**
- [FEATURE/ISSUE-XXX] - [What cannot proceed until this is fixed]

**Related Bugs:**
- [BUGFIX-XXX] - [How they're related]

**Requires:**
- [Code changes in other components]
- [Database migration]
- [Configuration changes]

---

## 📊 Validation Criteria

**Fix is complete when:**

1. **Bug is Fixed:**
   - [ ] Reproduction steps no longer trigger bug
   - [ ] Expected behavior occurs consistently
   - [ ] No error messages appear

2. **Tests Pass:**
   - [ ] All new tests pass (bug fix specific)
   - [ ] All existing tests pass (no regressions)
   - [ ] Manual testing confirms fix
   - [ ] Edge cases handled

3. **Code Quality:**
   - [ ] Code follows style guidelines
   - [ ] Code reviewed and approved
   - [ ] No technical debt introduced
   - [ ] Documentation updated

4. **Deployment:**
   - [ ] Fix verified in staging environment
   - [ ] Rollback plan documented
   - [ ] Monitoring in place
   - [ ] Users notified (if applicable)

---

## 📈 Testing Requirements

**Unit Tests:**
- [ ] Test that reproduces the bug (should fail before fix)
- [ ] Test that verifies the fix (should pass after fix)
- [ ] Test edge cases related to the bug
- [ ] Test error handling
- [ ] Maintain/improve code coverage (≥90%)

**Integration Tests:**
- [ ] Test end-to-end workflow with fix
- [ ] Test integration points affected by fix
- [ ] Test with production-like data

**Manual Testing:**
- [ ] Follow exact reproduction steps
- [ ] Test variations of reproduction steps
- [ ] Test related features for regressions
- [ ] Test in different environments/browsers

**Performance Tests (if applicable):**
- [ ] Verify fix doesn't degrade performance
- [ ] Benchmark before and after fix

---

## 🚨 Hotfix Criteria

**Is this a hotfix?**
- [ ] Yes - Critical bug, requires immediate deployment
- [ ] No - Can wait for regular release cycle

**If Hotfix:**
- **User Impact:** [How many users affected]
- **Business Impact:** [Revenue/reputation impact]
- **Downtime:** [Is system down?]
- **Data Loss:** [Is data at risk?]
- **Security:** [Is it a security vulnerability?]

**Hotfix Process:**
1. [ ] Fix implemented and tested
2. [ ] Emergency code review completed
3. [ ] Deployed to staging and verified
4. [ ] Rollback plan ready
5. [ ] Deploy to production with monitoring
6. [ ] Post-deployment verification
7. [ ] Post-mortem scheduled

---

## 📝 Implementation Notes

**Key Implementation Points:**
1. [Important detail about fix]
2. [Important detail about fix]
3. [Important detail about fix]

**Configuration Changes:**
- [ ] Environment variables: [List any]
- [ ] Feature flags: [List any]
- [ ] Database changes: [List any]

**Deployment Considerations:**
- [ ] Database migration needed
- [ ] Service restart required
- [ ] Cache clear needed
- [ ] User notification needed

---

## 🔙 Rollback Plan

**If fix causes problems:**

**Rollback Steps:**
1. [Step to revert changes]
2. [Step to restore previous state]
3. [Step to verify rollback]

**Rollback Impact:**
- [What happens when rolled back]
- [How users are affected]
- [How long rollback takes]

**Alternative Mitigation:**
[If rollback not possible, how to mitigate]

---

## 📚 References

**Original Issue:**
- [ISSUE-XXX](../issues/ISSUE-XXX-issue-name.md)

**Related Documents:**
- [Requirements Documentation]
- [Architecture Documentation]
- [API Documentation]

**External Resources:**
- [Bug tracking system link]
- [User reports]
- [Error monitoring dashboard]

**Similar Bugs:**
- [Past bugs with similar symptoms]
- [Known issues in framework/library]

---

## 🔍 Post-Fix Analysis

**Lessons Learned:**
[What we learned from this bug]

**Prevention Strategy:**
1. **Process Improvement:** [How to prevent similar bugs]
2. **Testing Improvement:** [What tests were missing]
3. **Code Review:** [What to watch for]
4. **Monitoring:** [What alerts to add]

**Technical Debt:**
[Any technical debt that contributed to or remains after the fix]

---

## 💡 Additional Notes

[Any other relevant information]

---

**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD  
**Fixed By:** [Developer Name]  
**Verified By:** [QA Name]  
**Deployed:** YYYY-MM-DD
