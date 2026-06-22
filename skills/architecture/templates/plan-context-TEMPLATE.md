# Plan Context: {Project/Feature Name}

<!-- See skills/architecture/SKILL.md for how to fill. Style + caps: skills/project-conventions/SKILL.md#canonical-specs -->

## Technical stack

| Layer | Choice | ADR-Ref |
|---|---|---|
| Backend | {language, framework} | ADR-{nn} |
| Data | {database, ORM} | ADR-{nn} |
| Frontend | {framework, state} | ADR-{nn} |
| Infrastructure | {cloud, deploy, CI/CD} | ADR-{nn} |
| API and auth | {style, auth method} | ADR-{nn} |

## Architecture style

- Pattern: {Modular Monolith | Microservices | Serverless}
- Top quality goals: 1) {goal} 2) {goal} 3) {goal}

## ADR summary

| ADR | Title | Decision | Impact |
|---|---|---|---|
| ADR-{nn} | {title} | {decision} | High |
| ADR-{nn} | {title} | {decision} | Medium |

## External integrations

| System | Direction | Protocol | Purpose |
|---|---|---|---|
| {system} | Inbound \| Outbound | REST \| Events \| gRPC | {purpose} |

## Performance and security

| Aspect | Target | Source-ADR |
|---|---|---|
| Response time | {X} ms @ p{Y} | ADR-{nn} |
| Throughput | {Z} req/sec | ADR-{nn} |
| Authentication | {method} | ADR-{nn} |
| Authorization | {model} | ADR-{nn} |
| Encryption | at rest, in transit | ADR-{nn} |

## Dialog

Bidirectional channel between Coder and Architect. Not a blocker; only the change that depends on a pending question waits.

### Questions from Coder to Architect

| ID | Date | Question | Addressed by | Status |
|---|---|---|---|---|

### Answers from Architect

| ID | Date | Answer | Affected artifacts | Status |
|---|---|---|---|---|
