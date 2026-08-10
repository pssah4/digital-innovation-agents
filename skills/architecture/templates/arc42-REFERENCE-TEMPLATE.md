<!-- Written AFTER implementation, for auditors and customers who need
     a formal architecture document. Day-to-day answers live in
     src/ARCHITECTURE.map and the ADR catalog; this file may lag behind
     them and says so. Cap-exempt. Project file name:
     arc42-REFERENCE.md. Omit any section without substance. -->

# arc42 reference: {project}

> Post-code reference document. The wayfinder (`src/ARCHITECTURE.map`)
> and the ADR catalog are the canonical, current sources; this document
> is regenerated on demand and may lag behind them.

## 3. Context and scope

{C4 context: system, external actors, technical interfaces.}

| Interface | Protocol | Purpose |
|-----------|----------|---------|
| {interface} | {REST / events / ...} | {purpose} |

## 4. Solution strategy

| Decision | Technology | ADR |
|----------|------------|-----|
| {decision} | {technology} | ADR-{nn} |

Architecture style: {monolith / modular monolith / microservices /
serverless}. Quality approach: {one sentence}.

## 5. Building block view

{Level 1 context diagram; deeper levels only when they carry a
decision. The directory tree itself is NOT repeated here.}

## 6. Runtime view

{Only the flows that an auditor must understand; one sequence per
flow.}

## 7. Deployment view

{Environments, pipeline, artifact flow.}

## 9. Architecture decisions

| ADR | Title | Decision |
|-----|-------|----------|
| ADR-{nn} | {title} | {one-line summary} |
