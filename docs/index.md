---
layout: home
title: Digital Innovation Agents
titleTemplate: V-Model workflow for AI coding assistants

hero:
  text: |
    When code costs almost nothing,
    the plan becomes the product.
  tagline: Shipping code is a solved problem. What most teams still lack is evidence that the features they ship matter to a real user. This workflow unites structured user discovery, tech-agnostic requirements, architecture decisions, a quality-gated coding loop, testing, and a security audit in one workflow, so your AI never builds the wrong thing at speed.
  actions:
    - theme: brand
      text: Get Started
      link: /tutorials/installation
    - theme: alt
      text: Full V-Model walkthrough
      link: /tutorials/full-v-model-run
---

<div class="landing-features">
  <a class="tile" href="/digital-innovation-agents/tutorials/first-business-analysis">
    <h3>Starting from a raw idea?</h3>
    <p>Walk the AI through structured discovery: personas, Jobs to be Done, How-Might-We questions. Twenty proven innovation methods before a single line of code.</p>
    <span class="arrow">Run your first Business Analysis →</span>
  </a>
  <a class="tile" href="/digital-innovation-agents/guides/reverse-engineering">
    <h3>Starting with an existing project?</h3>
    <p>Walk the V backwards. Reverse-engineer ADRs, an arc42 snapshot, a FEATURE inventory, and an evidence-based BA draft from your code. Every claim sourced, nothing invented.</p>
    <span class="arrow">Run Reverse Engineering →</span>
  </a>
</div>

<div class="landing-diagram">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 460" role="img" aria-labelledby="vm-title vm-desc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',sans-serif" preserveAspectRatio="xMidYMid meet">
  <title id="vm-title">V-Model workflow for AI coding assistants</title>
  <desc id="vm-desc">Click any phase, method, or loop to jump to its documentation.</desc>
  <defs>
    <marker id="arrow-handoff" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0 0 L10 5 L0 10 Z" fill="#f97316"/>
    </marker>
    <marker id="arrow-loop" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0 0 L10 5 L0 10 Z" fill="#94a3b8"/>
    </marker>
  </defs>

  <a href="/digital-innovation-agents/guides/business-analyse">
    <rect x="30" y="15" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="110" y="31" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Users · Needs · Market</text>
    <rect x="30" y="45" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="110" y="61" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">JTBD · Hypotheses</text>
    <rect x="30" y="75" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="110" y="91" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Pricing · Viability</text>
    <rect x="20" y="115" width="180" height="120" rx="16" fill="#be185d" stroke="#f9a8d4" stroke-width="2.5"/>
    <text x="110" y="155" text-anchor="middle" font-size="24" font-weight="700" fill="#fdf2f8">Business</text>
    <text x="110" y="187" text-anchor="middle" font-size="24" font-weight="700" fill="#fdf2f8">Analysis</text>
    <text x="110" y="215" text-anchor="middle" font-size="14" fill="#fbcfe8">Why</text>
    <rect x="30" y="250" width="160" height="65" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="110" y="276" text-anchor="middle" font-size="15" fill="#475569">BA doc</text>
    <text x="110" y="300" text-anchor="middle" font-size="15" fill="#475569">Exploration board</text>
  </a>

  <a href="/digital-innovation-agents/guides/requirements-engineering">
    <rect x="234" y="15" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="314" y="31" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Epic from HMW</text>
    <rect x="234" y="45" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="314" y="61" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">User stories (F/E/S)</text>
    <rect x="234" y="75" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="314" y="91" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Validation criteria</text>
    <rect x="224" y="115" width="180" height="120" rx="16" fill="#be185d" stroke="#f9a8d4" stroke-width="2.5"/>
    <text x="314" y="155" text-anchor="middle" font-size="24" font-weight="700" fill="#fdf2f8">Requirements</text>
    <text x="314" y="187" text-anchor="middle" font-size="24" font-weight="700" fill="#fdf2f8">Engineering</text>
    <text x="314" y="215" text-anchor="middle" font-size="14" fill="#fbcfe8">What</text>
    <rect x="234" y="250" width="160" height="65" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="314" y="276" text-anchor="middle" font-size="15" fill="#475569">Epics · Features</text>
    <text x="314" y="300" text-anchor="middle" font-size="15" fill="#475569">Backlog · Handoff</text>
  </a>

  <a href="/digital-innovation-agents/guides/architecture">
    <rect x="438" y="15" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="518" y="31" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">ADR (MADR)</text>
    <rect x="438" y="45" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="518" y="61" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">arc42</text>
    <rect x="438" y="75" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="518" y="91" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">plan-context</text>
    <rect x="428" y="115" width="180" height="120" rx="16" fill="#be185d" stroke="#f9a8d4" stroke-width="2.5"/>
    <text x="518" y="172" text-anchor="middle" font-size="24" font-weight="700" fill="#fdf2f8">Architecture</text>
    <text x="518" y="205" text-anchor="middle" font-size="14" fill="#fbcfe8">How</text>
    <rect x="438" y="250" width="160" height="65" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="518" y="276" text-anchor="middle" font-size="15" fill="#475569">ADRs · arc42</text>
    <text x="518" y="300" text-anchor="middle" font-size="15" fill="#475569">plan-context</text>
  </a>

  <a href="/digital-innovation-agents/guides/coding">
    <rect x="642" y="15" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="722" y="31" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Codebase review</text>
    <rect x="642" y="45" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="722" y="61" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">TDD · Debugging</text>
    <rect x="642" y="75" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="722" y="91" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Verification gate</text>
    <rect x="632" y="115" width="180" height="120" rx="16" fill="#7e22ce" stroke="#d8b4fe" stroke-width="2.5"/>
    <text x="722" y="172" text-anchor="middle" font-size="24" font-weight="700" fill="#faf5ff">Coding</text>
    <text x="722" y="205" text-anchor="middle" font-size="14" fill="#e9d5ff">Enhanced default agent</text>
    <rect x="642" y="250" width="160" height="65" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="722" y="276" text-anchor="middle" font-size="15" fill="#475569">Source code</text>
    <text x="722" y="300" text-anchor="middle" font-size="15" fill="#475569">Bug log</text>
  </a>

  <a href="/digital-innovation-agents/guides/testing">
    <rect x="846" y="15" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="926" y="31" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">AAA · FIRST</text>
    <rect x="846" y="45" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="926" y="61" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Unit + integration</text>
    <rect x="846" y="75" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="926" y="91" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Coverage targets</text>
    <rect x="836" y="115" width="180" height="120" rx="16" fill="#4338ca" stroke="#a5b4fc" stroke-width="2.5"/>
    <text x="926" y="172" text-anchor="middle" font-size="24" font-weight="700" fill="#eef2ff">Testing</text>
    <text x="926" y="205" text-anchor="middle" font-size="14" fill="#c7d2fe">UT + IT</text>
    <rect x="846" y="250" width="160" height="65" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="926" y="276" text-anchor="middle" font-size="15" fill="#475569">Test suites</text>
    <text x="926" y="300" text-anchor="middle" font-size="15" fill="#475569">Coverage</text>
  </a>

  <a href="/digital-innovation-agents/guides/security-audit">
    <rect x="1050" y="15" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="1130" y="31" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">OWASP Top 10</text>
    <rect x="1050" y="45" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="1130" y="61" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">LLM · SAST · SCA</text>
    <rect x="1050" y="75" width="160" height="24" rx="12" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="1130" y="91" text-anchor="middle" font-size="13" font-weight="500" fill="#334155">Zero Trust</text>
    <rect x="1040" y="115" width="180" height="120" rx="16" fill="#164e63" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="1130" y="155" text-anchor="middle" font-size="24" font-weight="700" fill="#e0f2fe">Security</text>
    <text x="1130" y="187" text-anchor="middle" font-size="24" font-weight="700" fill="#e0f2fe">Audit</text>
    <text x="1130" y="215" text-anchor="middle" font-size="14" fill="#7dd3fc">OWASP · LLM · SCA</text>
    <rect x="1050" y="250" width="160" height="65" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="1130" y="276" text-anchor="middle" font-size="15" fill="#475569">Audit report</text>
    <text x="1130" y="300" text-anchor="middle" font-size="15" fill="#475569">Backlog updates</text>
  </a>

  <line x1="206" y1="175" x2="218" y2="175" stroke="#f97316" stroke-width="3.5" marker-end="url(#arrow-handoff)"/>
  <line x1="410" y1="175" x2="422" y2="175" stroke="#f97316" stroke-width="3.5" marker-end="url(#arrow-handoff)"/>
  <line x1="614" y1="175" x2="626" y2="175" stroke="#f97316" stroke-width="3.5" marker-end="url(#arrow-handoff)"/>
  <line x1="818" y1="175" x2="830" y2="175" stroke="#f97316" stroke-width="3.5" marker-end="url(#arrow-handoff)"/>
  <line x1="1022" y1="175" x2="1034" y2="175" stroke="#f97316" stroke-width="3.5" marker-end="url(#arrow-handoff)"/>

  <line x1="110" y1="235" x2="110" y2="250" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="314" y1="235" x2="314" y2="250" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="518" y1="235" x2="518" y2="250" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="722" y1="235" x2="722" y2="250" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="926" y1="235" x2="926" y2="250" stroke="#cbd5e1" stroke-width="1.5"/>
  <line x1="1130" y1="235" x2="1130" y2="250" stroke="#cbd5e1" stroke-width="1.5"/>

  <a href="/digital-innovation-agents/guides/testing">
    <path d="M 885 319 L 885 360 L 772 360 L 772 319" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#arrow-loop)"/>
    <text x="828" y="380" text-anchor="middle" font-size="14" font-style="italic" font-weight="500" fill="#6b7280">Test fix loop</text>
  </a>

  <a href="/digital-innovation-agents/guides/security-audit">
    <path d="M 1085 319 L 1085 405 L 730 405 L 730 319" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#arrow-loop)"/>
    <text x="907" y="425" text-anchor="middle" font-size="14" font-style="italic" font-weight="500" fill="#6b7280">Security fix loop</text>
  </a>

  <a href="/digital-innovation-agents/concepts/living-documents">
    <path d="M 680 319 L 680 405 L 314 405 L 314 319" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#arrow-loop)"/>
    <text x="497" y="425" text-anchor="middle" font-size="14" font-style="italic" font-weight="500" fill="#6b7280">Living documents writeback</text>
  </a>
</svg>
</div>
