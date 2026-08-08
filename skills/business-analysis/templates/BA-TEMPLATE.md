---
id: BA-{TARGET-ID}
title: {Title}
date: YYYY-MM-DD
target-type: project | epic | feat
target-id: {PROJECT | EPIC-NN | FEAT-EE-FF}
project-ba-ref: {path to BA-PROJECT.md, or omit for Project-BA itself}
scope: simple-test | poc | mvp
---

<!-- Five questions, answered from the dialog. The value is the dialog,
     not the document. Write only what was actually said or evidenced;
     never invent personas, percentages, or baselines. Optional long-form
     sections live in BA-EXTENDED-TEMPLATE.md (separate file, written
     only on request). Cap: 40 lines. -->

# Business Analysis: {Title}

## 1. Problem (observed)

{What hurts today, for whom, how often. Quantify only with real
observations; "unknown" is a valid value.}

## 2. Who has it

{The affected users/roles in one or two sentences. Reference Project-BA
personas by ID when they exist; do not redefine them here.}

## 3. Solution hypothesis and strongest assumption

{One sentence solution hypothesis. How might we {goal} despite
{obstacle}?}
Assumption: {the one assumption that, if wrong, invalidates this BA.}

## 4. Scope

- In: {capability 1}, {capability 2}
- Out: {excluded 1}, {excluded 2}

## 5. Success signal and top risk

- Signal: {how we will notice it works; a number only if a baseline exists}
- Risk: {the biggest risk and its mitigation}
