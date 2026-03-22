# Tech-Agnostic Success Criteria -- Verbotene Begriffe

Diese Begriffe duerfen NICHT in der "Success Criteria (Tech-Agnostic)" Section
von Features erscheinen. Sie gehoeren in die "Technical NFRs" Section.

## Authentication / Authorization

OAuth, JWT, SAML, OpenID, OIDC, Bearer, Token, RBAC, ABAC

## API / Protocol

REST, GraphQL, gRPC, WebSocket, HTTP, HTTPS, API, JSON, XML, YAML,
endpoint, request, response, webhook

## Database

SQL, NoSQL, PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch,
DynamoDB, query, index, table, schema

## Frontend

React, Angular, Vue, Svelte, JavaScript, TypeScript, CSS, HTML,
DOM, component, state management

## Backend

Python, Java, Node, FastAPI, Express, Spring, Django, Flask,
microservice, serverless, lambda

## Infrastructure

Docker, Kubernetes, K8s, AWS, Azure, GCP, container, pod, cluster,
load balancer, CDN

## Performance (technical)

ms, millisecond, latency, throughput, req/sec, cache, caching,
Redis, Memcached, p95, p99

## Security (technical)

TLS, SSL, AES, encryption, hash, bcrypt, firewall, WAF

## Messaging

Kafka, RabbitMQ, SQS, pub/sub, message queue, event-driven, async

## Transformation Guide

| Technical (verboten) | Tech-Agnostic (erlaubt) |
|----------------------|-------------------------|
| Response time < 200ms | Users experience sub-second response |
| OAuth 2.0 authentication | Secure authentication using industry standards |
| PostgreSQL with indexes | System efficiently handles 100K+ records |
| REST API with JSON | Machine-readable interface for integrations |
| 99.9% uptime SLA | System available during business hours with minimal interruptions |
| Redis caching | Frequently accessed data loads instantly |
| RBAC authorization | Users only see data relevant to their role |
| TLS 1.3 encryption | Data transmitted securely |
| Kubernetes auto-scaling | System handles traffic spikes without degradation |
| WebSocket real-time | Users see updates without refreshing |
