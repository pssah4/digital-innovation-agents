---
title: Tech-agnostic Requirements
description: The rule that Success Criteria must be technology-neutral, with a forbidden-terms list and concrete transformation examples.
---

# Tech-agnostic Requirements

Digital Innovation Agents enforces a strict rule in Phase 2
(Requirements Engineering): Success Criteria must be technology-neutral.
Technology choices belong in a separate "Technical NFRs" section, which
feeds Phase 3 (Architecture).

## Why this matters

When a Success Criterion says "OAuth 2.0 authentication with JWT
tokens", the spec has already locked in a technology before the
architect has made the decision. That is:

- **Premature**: the technical choice was made without architecture review
- **Fragile**: the architect is boxed in. If OAuth does not fit,
  the Feature spec itself has to change.
- **Opaque**: the spec hides why authentication matters and what
  the user-facing outcome is

The fix is simple. Success Criteria describe user-facing outcomes.
Technical NFRs describe implementation constraints. Architecture
translates NFRs into ADRs.

## The separation

| Success Criteria | Technical NFRs |
|---|---|
| What the user gets | How it is built |
| Measurable, verifiable | Technology choices, concrete numbers |
| Tech-neutral | Tech-specific |
| Example: "Users are authenticated securely" | Example: "Auth via OAuth 2.0 / Azure AD B2C" |
| Example: "System handles 100K concurrent users" | Example: "PostgreSQL 15 with read replicas" |

## Forbidden terms in Success Criteria

Success Criteria may not contain any of these (non-exhaustive list):

- **Auth / Security**: OAuth, JWT, SAML, OIDC, TLS, RBAC, mTLS
- **Databases**: SQL, NoSQL, PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
- **Frontend**: React, Vue, Angular, Svelte
- **Backend**: Python, Node, Java, Go, Rust, Spring, FastAPI
- **Protocols**: REST, GraphQL, gRPC, HTTP, WebSocket, SSE, WebRTC
- **Cloud / Ops**: AWS, Azure, GCP, Docker, Kubernetes, Terraform, CI/CD
- **Data formats**: JSON, YAML, XML, Protobuf, Avro
- **Performance**: "milliseconds", "< 200ms", "p95", "throughput"
- **Caching**: "cache", "Redis cache", "CDN"
- **Messaging**: Kafka, RabbitMQ, SQS, Kinesis

See `skills/requirements-engineering/references/tech-agnostic-rules.md`
for the complete, enforced list.

## Transformation examples

| Forbidden (tech-specific) | Allowed (tech-agnostic) |
|---|---|
| "Response time < 200ms" | "Users experience sub-second response" |
| "OAuth 2.0 authentication" | "Secure authentication using industry standards" |
| "PostgreSQL with indexes" | "System efficiently handles 100K+ records" |
| "REST API with JSON" | "Machine-readable interface for integrations" |
| "99.9% uptime SLA" | "System available during business hours" |
| "Redis caching" | "Frequently accessed data loads instantly" |
| "RBAC authorization" | "Users only see data relevant to their role" |
| "WebSocket real-time" | "Users see updates without refreshing" |
| "Processing takes < 5 seconds" | "Users receive results without perceivable delay" |

## Where the forbidden terms go

Nothing is lost. The tech terms move from Success Criteria to the
**Technical NFRs** section of the same Feature file. Example:

```markdown
## Success Criteria
- SC-01: Users are authenticated securely using industry standards.
- SC-02: User sessions persist across browser restarts without
  requiring re-login.

## Technical NFRs
- **Security**: OAuth 2.0 / OIDC via Azure AD B2C. JWT tokens with
  15-minute access and 7-day refresh.
- **Session persistence**: HttpOnly cookies with Secure + SameSite=Strict.
```

The architect sees both when creating ADRs. The business side sees
only the SC: clean, user-outcome-focused, verifiable.

## Enforcement in the skill

`/requirements-engineering` scans every Success Criterion for
forbidden terms before writing the Feature file. If a term is found,
the skill prompts the user to rephrase:

```
FEATURE-001-003 SC-03 contains "PostgreSQL". That's a technology term.
Let's move it to Technical NFRs.

Rewrite SC-03 as a user-facing outcome. Example: "System efficiently
handles 100K+ records without data loss."

Should I update the file?
```

## When the rule does not apply

Technical NFRs contain tech terms. That is the point. The forbidden
list is only for Success Criteria, not for Technical NFRs, Definition
of Done, or ADRs.

## Benefits

- **Decouples business from implementation**: Success Criteria stay
  stable even if the architect changes the tech choice
- **Keeps the spec readable** for non-technical stakeholders
- **Forces explicit architecture decisions**: tech choices must have
  an ADR, not just a mention in a Feature file
- **Enables traceability**: every SC traces to a user-facing benefit,
  not an implementation detail

## See also

- [Requirements Engineering guide](../guides/requirements-engineering)
- [V-Model concept](./v-model): the phase where SC and NFR split matters
