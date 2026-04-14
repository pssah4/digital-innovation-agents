# Innovation Methods Catalog

Purpose. This is a trigger-to-method lookup for the BA and RE skills. When a gap appears in the user's input (missing persona, missing need, missing evidence, missing constraint), the agent stops asking questions and proposes the matching method from this catalog. Each entry links to the full method card in the VitePress docs under `docs/reference/methods-*.md`, which is where the user will read the practical details.

The actual work (interviews, observations, tests, shadowing) always stays with the user. The agent's job is to pick the right method, explain it in one paragraph, and help the user prepare the artifact they need.

## How to propose a method in the dialog

When a gap appears, do not keep asking the same question in different words. Switch to a method proposal.

Dialogue template:

> "To answer that properly, we need [evidence from real users / input from experts / a quick prototype]. The method that fits here is **{METHOD}**. {one or two sentences about what it produces}. Team and time: {X}. Full card: {doc link}. Shall I help you prepare {concrete next step, e.g. an interview guideline, a question list, a test grid}?"

After the user agrees, help them prepare the artifact (interview questions, observation plan, prototype brief, test grid), tell them what to bring back, and pause the interview. Resume when they return with findings.

## Discovery methods (understand users and the problem space)

Full cards: `docs/reference/methods-discovery.md`

### Qualitative interview

**Trigger:** The user cannot describe the user concretely. Their own answers to "why is that a problem" feel like guesses.
**Nutshell:** An open, narrative-driven conversation with one user. Two people per session (moderator + note-taker), 60 to 90 minutes, open questions only, transcribe verbatim, extract four or five raw observations within 30 minutes of finishing.
**Doc link:** `methods-discovery#qualitative-interview`

### Explorative interviews

**Trigger:** The problem space is fuzzy. Several user groups might be affected but cannot be ranked. The user wants to verify the problem exists at all before investing in deep research.
**Nutshell:** 7 to 10 short conversations, 20 to 30 minutes each, across users with no prior relationship. Cluster the surprises after the batch to decide where to go deep.
**Doc link:** `methods-discovery#explorative-interviews`

### Extreme users

**Trigger:** Average-user interviews produce generic answers. The user group feels too uniform. No emotional driver has surfaced.
**Nutshell:** Interview two to four power users (who do the thing 10x more than average) and two to four non-users (who tried it and quit). Their combined motivations and objections bracket the real design space.
**Doc link:** `methods-discovery#extreme-users`

### Expert conversations

**Trigger:** The problem has regulatory, technical, or safety implications the user cannot evaluate alone. Stakeholders disagree on what is possible.
**Nutshell:** Specific-question interview with a domain expert. 30 to 45 minutes. Pick the expert for one question, not a general brain pick.
**Doc link:** `methods-discovery#expert-conversations`

### Fly on the wall

**Trigger:** Users describe an ideal workflow that contradicts reality. They cannot describe a routine they consider too obvious to mention.
**Nutshell:** Silent, non-intrusive observation of real behaviour in a real context. At least 60 minutes. Three columns of notes: what they do, what they work around, where they hesitate.
**Doc link:** `methods-discovery#fly-on-the-wall`

### Self-test (immersion)

**Trigger:** The user has never personally experienced the problem. Interview questions sound generic. Assumptions about "how easy" or "how hard" need testing.
**Nutshell:** Walk the user's process first-hand. One hour to several days. Log friction points as they happen, debrief within 24 hours, then verify conclusions with real users.
**Doc link:** `methods-discovery#self-test`

### Cultural probes

**Trigger:** The behaviour of interest happens in private or is spread over days or weeks. Users self-censor the relevant moments in live interviews.
**Nutshell:** A light kit (diary, photo prompts, a few tasks) sent home with four to six users for one or two weeks. A 45-minute debrief per participant about their own artifacts.
**Doc link:** `methods-discovery#cultural-probes`

### User motivation analysis

**Trigger:** Interview notes exist but the user cannot name what the user actually wants. Needs sound the same. No ranking of intensity.
**Nutshell:** Cluster raw insights, split each cluster into functional needs, emotional needs, and obstacles, then rank by frequency times intensity. Two to four people, two or three hours.
**Doc link:** `methods-discovery#user-motivation-analysis`

### Persona synthesis cluster

**Trigger:** Too much interview data to fold into a single persona. Users clearly fall into several groups. Not ready for final personas yet.
**Nutshell:** Affinity-cluster every insight by behaviour (not demographic), name each cluster in one short phrase, draft a persona seed per cluster.
**Doc link:** `methods-discovery#persona-synthesis-cluster`

### Persona

**Trigger:** A persona seed exists. Design decisions drift because the user is too abstract. Team members hold different mental models of the same user.
**Nutshell:** One named, vivid persona backed by interview evidence. Goals, motivations, frustrations, typical day, one direct quote. One page maximum.
**Doc link:** `methods-discovery#persona`

### Value proposition chain

**Trigger:** The project is B2B and the buyer is not the end user. Value passes through several hands. You suspect the wrong actor is getting paid.
**Nutshell:** Map every actor in a line, label the value and friction at each hand-off, mark where value leaks, pick the most underserved actor as the primary persona.
**Doc link:** `methods-discovery#value-proposition-chain`

### Research mind map

**Trigger:** The problem is too broad to interview anyone about. Several researchers are splitting work and need alignment on scope.
**Nutshell:** Radial decomposition of a central question into four to six research fields and their sub-questions. Prioritise fields, assign owners.
**Doc link:** `methods-discovery#research-mind-map`

### Stakeholder map

**Trigger:** The project touches several departments or external parties. Interviews are about to start but it is unclear who to talk to. Political friction suspected.
**Nutshell:** Every actor on a sticky. Place on an influence-by-interest matrix. Draw labelled relationships. High-influence + low-interest is the most dangerous cell.
**Doc link:** `methods-discovery#stakeholder-map`

### Market and trend analysis

**Trigger:** Competitors cannot be named. The project risks obsolescence from an underlying trend. The user wants to find adjacent opportunities.
**Nutshell:** Desk research, cluster into four to six themes, place competitors inside, write a one-sentence potential field per cluster.
**Doc link:** `methods-discovery#market-and-trend-analysis`

### User journey

**Trigger:** The user's experience spans several touchpoints. The pain lives in one phase of usage rather than the product itself.
**Nutshell:** Stage-by-stage map with four lanes (actions, thoughts, emotions, touchpoints). Draw an emotion line. Dips show where to intervene.
**Doc link:** `methods-discovery#user-journey`

## Ideation methods (generate and sharpen ideas)

Full cards: `docs/reference/methods-ideation.md`

### Brainstorming

**Trigger:** A sharp HMW exists and the solution space is empty. The team has not yet tried to solve the problem together.
**Nutshell:** Group ideation session, 15 to 20 minutes, one HMW, one post-it per idea, the eleven Design Thinking rules enforced. Cluster without evaluation at the end.
**Doc link:** `methods-ideation#brainstorming`

### Brainwriting

**Trigger:** Previous brainstorms were dominated by one or two voices. The team is introverted. Seed ideas exist and need to travel through several hands.
**Nutshell:** Silent ideation. Six people, a 3x6 grid per person, three minutes per row, pass the sheet, build on what the previous person wrote. 30 minutes total.
**Doc link:** `methods-ideation#brainwriting`

### Idea tower

**Trigger:** A seed idea is promising but too thin to prototype. The team keeps saying "yes and we would need X" without closing the loop.
**Nutshell:** Additive-only enrichment of a single idea. Each person adds one element per round. Only adds, no removals. 20 to 30 minutes.
**Doc link:** `methods-ideation#idea-tower`

### Collective notebook

**Trigger:** The problem is complex and one-hour workshops produce shallow ideas. The team needs time to let the problem sit.
**Nutshell:** One notebook per person, one or two weeks, log any idea when it surfaces. Mid-period share keeps people engaged. Single synthesis session at the end.
**Doc link:** `methods-ideation#collective-notebook`

### Inspiration cards

**Trigger:** The team is repeating variations of the same three or four ideas. Forced unfamiliar associations are needed.
**Nutshell:** A random deck of 20 to 40 cards (words, images, products from unrelated domains). Draw three or four, generate ideas that connect each card to the HMW.
**Doc link:** `methods-ideation#inspiration-cards`

### Idea clustering and selection

**Trigger:** 30 to 50 ideas on the wall and no obvious shortlist. Team members advocate different candidates by preference.
**Nutshell:** Cluster by theme, pick at most four criteria (User Value, Feasibility, Transferability, Risk), score on 0-5, pick the top three. Use the scores as an aid, not a verdict.
**Doc link:** `methods-ideation#idea-clustering-and-selection`

### Jobs to be done

**Trigger:** An idea exists but the user cannot explain why users would switch. User stories cover only the functional layer.
**Nutshell:** For the target user, answer the functional, emotional, and social job. Name hiring criteria (reasons to switch) and firing criteria (reasons to abandon).
**Doc link:** `methods-ideation#jobs-to-be-done`

### TRIZ

**Trigger:** A genuine technical contradiction ("strong and light", "fast and safe"). Conventional brainstorming only produces incremental variants.
**Nutshell:** State the contradiction precisely, look up the matching inventive principles in the TRIZ contradiction matrix, generate one idea per principle.
**Doc link:** `methods-ideation#triz`

### Kill your company

**Trigger:** Team is too close to the current product to see its weaknesses. Competitive threats are vague.
**Nutshell:** Flip the frame. The team pretends to be a startup attacking the company. Brainstorm attacks, rank by plausibility, write the defence, identify the missing defences.
**Doc link:** `methods-ideation#kill-your-company`

## Validation methods (test ideas and the business)

Full cards: `docs/reference/methods-validation.md`

### Wireframes, storyboards, and paper prototypes

**Trigger:** An idea needs early user feedback before any code is written. The team debates the concept and a picture would end the debate faster than another meeting.
**Nutshell:** Low-fidelity sketches of the risky part only. Put in front of a user, watch where they hesitate, iterate.
**Doc link:** `methods-validation#wireframes-storyboards-and-paper-prototypes`

### Appearance prototype

**Trigger:** Functional design is clear, visual direction is not. Brand, aesthetics, and trust need testing before flow is finalised.
**Nutshell:** One to three polished visual variants, no functionality. Show each for 10 seconds cold. Capture first-impression words verbatim, then interview.
**Doc link:** `methods-validation#appearance-prototype`

### Context and system prototypes

**Trigger:** Success depends on the environment (noisy shop floor, one-handed kitchen, shared family device, integration with other tools). Real friction lives in the hand-offs.
**Nutshell:** Smallest version that survives the real context. Deploy for days or weeks. Observe or log from inside the context, not afterwards.
**Doc link:** `methods-validation#context-and-system-prototypes`

### Wizard of Oz

**Trigger:** The feature is expensive to build (AI, automation, backend-heavy) and you want to see if users would even use it. You want to test the interaction pattern, not the technology.
**Nutshell:** Build the visible surface, put a human behind it to generate responses in real time. 30 to 45 minutes per user, six to eight users. Debrief for expectations.
**Doc link:** `methods-validation#wizard-of-oz`

### Card sorting

**Trigger:** Menu, taxonomy, or content hierarchy confuses users. About to commit to a new navigation structure.
**Nutshell:** 30 to 60 cards, users group them into clusters (open or closed sort), user-generated cluster names become navigation labels. Five to eight users.
**Doc link:** `methods-validation#card-sorting`

### Test grid

**Trigger:** Multiple prototype sessions and findings pile up in different formats. Patterns need to appear across sessions.
**Nutshell:** Grid with criteria as rows, one column per user session. Fill cells with direct observations, scan rows horizontally for patterns.
**Doc link:** `methods-validation#test-grid`

### Expert review

**Trigger:** Feasibility question is "can this even exist" rather than "do users want this". Regulatory or technical sanity check before a deeper test.
**Nutshell:** 30 to 45 minutes with a specific expert, a one-page summary and three focused questions. Capture vocabulary verbatim for the later ADR.
**Doc link:** `methods-validation#expert-review`

### Business plan

**Trigger:** Idea passed user testing. Revenue, cost, and business-model assumptions need surfacing.
**Nutshell:** Business Model Canvas fields filled with one sentence each. Every revenue and cost cell gets a number, however rough. Mark unsupported assumptions as next hypotheses.
**Doc link:** `methods-validation#business-plan`

### Value proposition quantification

**Trigger:** Two or three value propositions compete and the team debates which to commit to. Baseline needed before user tests.
**Nutshell:** Break the VP into four to six dimensions (activation, preference, willingness to pay, willingness to recommend), score each 0 to 10 against existing evidence, pick the weakest dimension as the next test target.
**Doc link:** `methods-validation#value-proposition-quantification`

### Pre-mortem

**Trigger:** Team is too optimistic. Stakeholders about to commit resources. Planning conversation is not surfacing risks.
**Nutshell:** "It is six months from now and this project has failed. Write down why." Five minutes silent writing per person. Cluster reasons, write preventive actions, assign owners to the top three or four.
**Doc link:** `methods-validation#pre-mortem`

## Probing techniques (inside interviews)

These work in both directions. The user uses them on field interview partners. The agent uses them on the user when answers go thin.

### 5-Why

Ask "why is that a problem?" up to five times. You do not always get to five. You almost always get past the first surface answer.

### Concretisation

"Can you give me a concrete example?"
"When was the last time this happened?"
"Show me how you did that."

### Future projection

"Imagine the problem was solved tomorrow. What changes?"
"What would your ideal day look like in two years?"
"What would need to happen for you to say: yes, this is exactly what I need?"

### Perspective shift

"What would your customer say about this?"
"What would your boss say?"
"How does a completely different industry solve this?"

### Emotional level

"How did that feel?"
"What frustrated you most?"
"What would delight you about the alternative?"

### Analogy trigger

"Do you know something similar from another domain?"
"Where have you seen this pattern before?"
"If this was a physical product, what would it look like?"

### Contrast

"What if it were exactly the opposite?"
"What would the worst case look like?"
"If budget were not a constraint, what then?"

## Anti-patterns

- Proposing a method without a trigger. If the user's input is sufficient, keep going. Do not pad the session.
- Proposing a heavy method when a lighter one would work. Explorative interviews before qualitative interviews. Self-test before cultural probes.
- Skipping the preparation step. After proposing a method, help the user prepare the artifact (interview questions, observation plan, test grid). Do not dump the name and disappear.
- Running the method yourself. The agent never runs interviews, observations, or tests. It prepares and it synthesises. The user runs the method.

## Relationship between catalog and doc cards

The catalog on this page is the trigger logic the agent loads at runtime. The doc method cards are the user-facing version with step-by-step guidance, timings, tips, and the "what to bring back" checklist. When the agent proposes a method, it always links to the matching doc card so the user can open the practical detail.

Mapping:

- Discovery catalog entries link to `docs/reference/methods-discovery.md#{anchor}`
- Ideation catalog entries link to `docs/reference/methods-ideation.md#{anchor}`
- Validation catalog entries link to `docs/reference/methods-validation.md#{anchor}`

Anchors use VitePress slug rules. Lowercase, spaces to hyphens, parentheses dropped.
