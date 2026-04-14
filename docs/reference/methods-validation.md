---
title: Validation methods
description: Method cards for testing, prototyping, and validating ideas with real users. The Business Analysis agent proposes these when a shortlist of ideas exists but the riskiest assumptions are not yet tested.
---

# Validation methods

Once you have ideas, the next question is which ones actually work when a real person touches them. Validation is the part where assumptions meet users, and where ideas that sound brilliant in a workshop quietly collapse. The [Business Analysis skill](../guides/business-analyse) will propose the validation method that matches the riskiest assumption, not the easiest one.

Testing happens between humans. You put a prototype in front of a user, watch what they do, and come back with observations the agent can turn into validated or invalidated hypotheses.

## Index

Prototype the experience

- [Wireframes, storyboards, and paper prototypes](#wireframes-storyboards-and-paper-prototypes)
- [Appearance prototype](#appearance-prototype)
- [Context and system prototypes](#context-and-system-prototypes)
- [Wizard of Oz](#wizard-of-oz)

Test with users

- [Card sorting](#card-sorting)
- [Test grid](#test-grid)
- [Expert review](#expert-review)

Test the business

- [Business plan](#business-plan)
- [Value proposition quantification](#value-proposition-quantification)
- [Pre-mortem](#pre-mortem)

## Wireframes, storyboards, and paper prototypes

Low-fidelity prototypes. Sketches on paper, storyboards showing the sequence of a scenario, rough mock-ups on screen. The goal is to make an idea tangible enough to react to without investing real development time.

**When to reach for it.** You have an idea and need early user feedback before building anything. The team is still arguing about the concept and a picture would end the debate faster than another meeting. You want users to react to the flow, not the visuals.

**How to run it.**

1. Pick the riskiest part of the experience. Do not try to prototype everything.
2. Sketch the screens, the steps, or the scenario on paper or in a lightweight tool. Rough is good. Ugly is good.
3. Put it in front of a user and ask them to walk through it. "What would you do next?"
4. Watch where they hesitate, where they guess, where they skip steps.
5. Iterate on the same session if it is quick enough.
6. Do a proper round of revisions afterwards, then test again.

**Team and time.** One or two people per session. 15 to 60 minutes per prototype. Plan at least three user sessions per variant.

**Things that go wrong.**

- Polishing the prototype too early. Users stop giving honest feedback once something looks finished.
- Prototyping the whole product instead of the risky part. Low fidelity means narrow scope.
- Explaining the prototype before the user tries it. If you have to explain it, the prototype is the problem.

**What to bring back to the agent.** The observations from the user sessions, the changes you made between iterations, and the remaining open questions.

## Appearance prototype

A visual-only prototype. It looks like the finished product but does nothing behind the surface. The only thing you are testing is how the product lands visually with users: does it attract, does it feel trustworthy, does it invite action.

**When to reach for it.** You have narrowed down the functional design and need to test brand, aesthetics, or visual hierarchy. A landing-page test would be premature because the flow is not finalised. You want to know if users find the product credible at first glance.

**How to run it.**

1. Design one to three visual variants of the product. Full-quality visuals, no functionality.
2. Print or present them to users for 10 seconds each. "What is this? Who is it for? Would you click?"
3. Capture the first-impression words verbatim.
4. Follow up with a short interview about why they used those words.
5. Compare the variants head-to-head to see which visual direction resonates.

**Team and time.** One designer plus one interviewer. 15 minutes per user. Five to eight users per variant.

**Things that go wrong.**

- Testing with people who already know what the product is. You lose the first-impression signal immediately.
- Letting users compare variants side by side from the start. Test each one cold first, then let them compare.
- Confusing appearance feedback with functional feedback. Keep the two tests separate.

**What to bring back to the agent.** The first-impression words, the variant that scored best, and the reasons users gave.

## Context and system prototypes

Prototypes that test the product in its real context or as part of a wider system, rather than in isolation. You are not testing the screen flow but how the product behaves in the actual usage environment.

**When to reach for it.** The product's success depends on the environment around it, not on the product itself (noisy factory floor, one-handed kitchen use, shared family device, cold garage). The product has to integrate with other tools or workflows and you need to see whether the integration points hold. You suspect the real friction lives in the hand-offs with other systems.

**How to run it.**

1. Build the smallest version of the product that can survive the real context.
2. Deploy it into that context for a few days or weeks.
3. Observe or log how it behaves. Collect user feedback from inside the context, not afterwards.
4. Look for integration failures, environmental friction, or workflow disruptions.
5. Iterate the prototype and redeploy.

**Team and time.** Two to four people. A few days to several weeks depending on the context.

**Things that go wrong.**

- Testing in a fake environment that does not reproduce the real friction. A kitchen at the office is not a kitchen at home.
- Ignoring the people around the user. In many contexts (families, shift teams, open-plan offices), the reactions of bystanders matter as much as the user's own experience.
- Skipping the logging. If you do not collect data from inside the context, you are relying on the user's memory, which is unreliable.

**What to bring back to the agent.** The integration points that failed, the environmental friction you observed, and the behaviour of bystanders.

## Wizard of Oz

A prototype that simulates a product feature with a human behind the curtain instead of real software. Users think they are interacting with a finished system. In reality, you are typing the answers in real time from the next room.

**When to reach for it.** The feature you want to test is expensive to build (AI, automation, complex backend) and you want to see if users would even use it before investing. You want to test the conversation or interaction pattern, not the underlying technology. You need real user behaviour against a realistic experience without shipping code.

**How to run it.**

1. Pick one user-facing flow to simulate. Keep it narrow.
2. Build the visible surface (a chat window, a form, a voice assistant) so the user sees a finished experience.
3. Put a team member on the other side to generate the responses in real time.
4. Run the session with the user, capturing every interaction and response time.
5. Debrief the user afterwards. Ask them what they expected, not what they saw.

**Team and time.** Two to three people, one of them operating the wizard. 30 to 45 minutes per session. Six to eight users.

**Things that go wrong.**

- Letting the wizard take too long to respond. Users notice and the illusion breaks.
- Scripting the wizard too tightly. The point is to see how the user reacts to realistic variability.
- Not debriefing. Without the debrief you learn behaviour but not expectation.

**What to bring back to the agent.** The interaction patterns the users actually used, the expectations they brought to the flow, and the places where the wizard struggled to respond quickly enough.

## Card sorting

A user test for information architecture. Users group labels (for menus, categories, content) into clusters that feel natural to them. It exposes where your proposed structure matches user mental models and where it does not.

**When to reach for it.** The product has a menu, a taxonomy, or a content hierarchy that users keep getting lost in. You are about to commit to a new navigation structure and want to pressure-test it first. You are localising a product and suspect the existing category names do not translate.

**How to run it.**

1. Write each item on a card. 30 to 60 cards is usually right.
2. Ask the user to group them into clusters that feel natural. Open sort (user names the clusters) or closed sort (clusters are pre-defined).
3. Watch which cards cause hesitation. Hesitation is where the vocabulary is wrong.
4. Ask the user to name each cluster they created. Their naming is your navigation label.
5. Repeat with five to eight users and look for convergence.

**Team and time.** One moderator, one note-taker. 30 to 45 minutes per user. Five to eight users.

**Things that go wrong.**

- Pre-writing the cluster names. You learn more from user-generated names.
- Mixing unrelated items on the same deck. The clusters become meaningless.
- Testing with one user and assuming the result generalises. Five users is the real minimum.

**What to bring back to the agent.** The most common clusters, the user-generated labels, and the cards that nobody could classify.

## Test grid

A structured evaluation sheet used during a prototype test with users. One row per test criterion, one column per user, with observations captured consistently so patterns appear across the sessions.

**When to reach for it.** You are running multiple prototype tests and the findings are piling up in different formats. You want to compare user reactions across sessions without losing the detail. You need to defend the test results to stakeholders later and freeform notes will not be enough.

**How to run it.**

1. Define the criteria before the test. What worked, what confused the user, what they asked for, what they liked.
2. Draw the grid with criteria as rows and one column per user session.
3. During each session, fill the cells with direct observations. Not conclusions, observations.
4. After all sessions, scan each row horizontally to spot patterns.
5. Mark the rows where the pattern is clear enough to act on.

**Team and time.** One note-taker per session. 15 minutes to set up. Filling the grid happens inside the normal test session.

**Things that go wrong.**

- Leaving cells empty because "the user did not mention it." Write down that the user did not mention it, that is also data.
- Writing conclusions instead of observations. Keep "the user said X" and "the user hesitated at Y" separate from "the user was confused."
- Designing the grid after the first two sessions. If you change the criteria mid-test, your columns are not comparable any more.

**What to bring back to the agent.** The filled grid and the rows where a clear pattern emerged.

## Expert review

A review session with one or two domain experts to pressure-test the feasibility of the solution. It is cheaper than a real prototype test and usually faster, but only as useful as the expert you pick.

**When to reach for it.** The solution has regulatory, technical, or safety implications and a user test would not surface them. You want a quick sanity check before investing in a Wizard of Oz or a paper prototype. The feasibility question is "can this even exist" rather than "do users want this."

**How to run it.**

1. Pick the expert for a specific question. "Would this comply with GDPR?" "Is this latency achievable?" "Would this break the existing integration?"
2. Prepare a one-page summary of the idea and the question.
3. Book 30 to 45 minutes.
4. Ask for the three biggest reasons the idea would fail as currently drawn.
5. Capture the exact vocabulary the expert uses. The vocabulary matters for the ADR later.

**Team and time.** One interviewer. 30 to 45 minutes. Two or three experts maximum.

**Things that go wrong.**

- Asking a general "what do you think" instead of a specific question. The answer will be useless.
- Accepting the expert's opinion as fact without asking what would change their mind. The ADR needs to record the counter-evidence as well.
- Using expert review as a substitute for user testing. It validates feasibility, not desirability.

**What to bring back to the agent.** The feasibility score broken into technical, organisational, financial, and the expert's exact phrasing on the main risks.

## Business plan

A traditional business plan or a one-page business-model canvas. Used to think through how the idea makes money, who pays whom, and what it costs to run. Not a prediction, a forcing function.

**When to reach for it.** The idea has passed user testing and the question is whether it can become a sustainable business. You want to surface revenue and cost assumptions before committing to an MVP. You are preparing to ask for funding and need a coherent story.

**How to run it.**

1. Fill in the nine fields of the Business Model Canvas: customer segments, value proposition, channels, customer relationships, revenue streams, key resources, key activities, key partners, cost structure.
2. For every cell, write one sentence. No long prose.
3. For the revenue and cost cells, put a number next to each line. Rough is fine, placeholder is not.
4. Pressure-test the story. "Does the revenue model match what the customer actually values?"
5. Mark the assumptions you cannot support with evidence. Those become the next hypotheses to test.

**Team and time.** Two to four people. 2 to 3 hours for a first draft.

**Things that go wrong.**

- Starting with revenue streams instead of customer segments. You will end up optimising for the wrong buyer.
- Writing prose in the cells. The whole point of the canvas is the discipline of short statements.
- Treating the first version as final. Redraft it after every user interview that changes your understanding.

**What to bring back to the agent.** The canvas, the critical assumptions you marked, and the cells where you could not fill in a number.

## Value proposition quantification

A structured scoring exercise for a value proposition. Instead of asking "is this good," you break the value proposition into measurable dimensions and rate each one. It exposes which parts of the proposition are weak.

**When to reach for it.** You have a value proposition and a shortlist of two or three candidates and need to compare them. The team is debating which proposition to commit to and needs an objective frame. You are preparing to test with users and want a baseline to measure against.

**How to run it.**

1. Break the value proposition into four to six dimensions. Common ones: activation (does it make users try it), preference over substitutes, willingness to pay, willingness to recommend.
2. Rate each dimension on a 0 to 10 scale, based on existing evidence from interviews and prototypes.
3. Mark the lowest dimension. That is the weakest link.
4. For each dimension, write the one thing that would move the score up by two points.
5. Use the scores as a baseline for the next round of user tests. Re-score after each round.

**Team and time.** The core BA team. 60 to 90 minutes.

**Things that go wrong.**

- Scoring from gut feeling with no evidence. The number means nothing unless it is tied to observations.
- Using too many dimensions. Four is usually enough. Six is the upper limit.
- Averaging the dimensions into a single number. You lose the signal. The weakest dimension is what matters.

**What to bring back to the agent.** The scores per dimension, the weakest dimension, and the planned test to improve it.

## Pre-mortem

An exercise where the team imagines the project has already failed and works backwards to explain why. It surfaces risks that nobody wants to mention in the normal planning conversation.

**When to reach for it.** The team is too optimistic and you sense the risks are being underplayed. Stakeholders are about to commit resources and you want one last pressure test. You are about to start implementation and want to catch the obvious failure modes before they become real.

**How to run it.**

1. Frame the scenario. "It is six months from now and this project has completely failed. Write down why."
2. Give each person five minutes of silent writing. One reason per line.
3. Collect all the reasons on the wall or in a shared doc.
4. Cluster the reasons into themes.
5. For each theme, write one preventive action you could take now.
6. Assign owners to the three or four actions that are most critical.

**Team and time.** The whole project team including the outsiders with context. 45 to 60 minutes.

**Things that go wrong.**

- Letting the session stay abstract. Push for specific failure modes, not "people will not use it."
- Skipping the preventive actions step. The scenarios are useless without a response.
- Running the pre-mortem too late. It has to happen before resources are locked in, otherwise the team is too invested to listen.

**What to bring back to the agent.** The three most likely failure modes and the preventive actions you committed to.

## Next steps

- When validation confirms a direction, the BA agent helps you turn the validated ideas into Critical Hypotheses and a handoff to [Requirements Engineering](../guides/requirements-engineering).
- For discovering user needs in the first place, see [Discovery methods](./methods-discovery).
- For generating and sharpening the ideas you are testing here, see [Ideation methods](./methods-ideation).
