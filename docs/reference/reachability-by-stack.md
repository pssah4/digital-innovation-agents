---
title: Reachability by stack
description: Per-language reference for the reachability check (/coding Phase 4a step 6) and the activation-path types (FEATURE Definition of Done). Covers TypeScript, JavaScript, Python, Go, Rust, React, R, plus an Obsidian-plugin TypeScript sub-profile.
---

# Reachability and Activation Path: per-stack reference

Operationalises the universal Done-definition contract from
[`/coding` Phase 4a Verification Gate](../guides/coding#phase-4a-verification-gate)
(steps 6 and 7) and the
[`/requirements-engineering` FEATURE subtype model](../guides/requirements-engineering#feature-subtype-since-v320).
The contract is universal; the tooling that verifies it is per
language.

This page mirrors `skills/coding/references/reachability-by-stack.md`
in the source repository. Each entry carries:

1. **Reachability tooling** -- concrete commands and scripts that
   report unused symbols and find callers. Run them from the project
   root.
2. **Activation path types** -- what counts as an activation path in
   this stack (the values you put after `Type:` in the FEATURE
   `## Activation Path` section).
3. **Cleanup pattern** -- stack-idiomatic teardown the coding skill
   should look for when listeners or resources are introduced.

The list grows by PR. If your stack is missing, copy the most similar
entry as a starting point and adjust.

## Configuration

Projects can declare their stack and a custom check in
`dia.config.json` at the project root:

```json
{
  "stack": "typescript-obsidian-plugin",
  "reachability_check": "tools/dia/check-reachability.sh"
}
```

If `stack` is set, the skill consults the matching row below.
If `reachability_check` is set, the skill executes that script and
parses its exit code (`0` = pass, non-zero = fail) and stdout.
If neither is set, the skill skips stack-specific checks with a notice
"no reachability tooling configured for stack=...".

The universal layer (Activation Path entry exists in the FEATURE spec,
Activation Path identifier present somewhere in the source tree as a
plain grep) always fires regardless of stack.

## TypeScript / Node

**Reachability tooling:**

- `npx ts-prune` finds exported symbols never imported elsewhere.
- `npx tsc --noUnusedLocals --noUnusedParameters` compiler-level
  unused-symbol report.
- `npx ts-morph` programmatic find-references for spot checks.
- `grep -rn "import.*from.*['\"]<module-path>['\"]" src/` for a quick
  caller spot-check on a specific symbol.

**Activation path types:**

`command`, `route`, `endpoint`, `scheduled-job`, `tool`, `public-API`.

**Cleanup pattern:**

`process.on('exit', ...)` for top-level cleanup;
`AbortController.signal.addEventListener('abort', ...)` for cancellable
async work; explicit `dispose()` / `close()` on sockets, file handles,
timers (`clearTimeout` / `clearInterval`).

## TypeScript: Obsidian Plugin sub-profile

A specialisation of the TypeScript entry. Adds plugin-specific
activation paths and the `onunload` cleanup contract.

**Reachability tooling:** TypeScript tooling above. Plus:

- `grep -rn "new <ClassName>" src/` -- the specific failure mode in
  Obsidian plugins is "class file exists, never instantiated".
- `grep -rn "<className>:" src/` -- for tools registered as
  `{ name: 'className', ... }` in a registry.

**Activation path types:**

- `command` registered via `this.addCommand({ id, name, callback })`
  in `main.ts` `onload`.
- `tool` registered in `ToolRegistry` AND added to a `TOOL_GROUPS`
  entry in `ToolExecutionPipeline` (the dual registration is the
  Obsilo pattern; both are mandatory).
- `UI-element` modal, side panel, status bar item, ribbon icon.
- `hotkey` registered as part of `addCommand` with a `hotkeys` array.
- `settings-toggle` option in the Settings tab; counts as an
  activation path because the user can flip it.
- `auto-trigger` `vault.on('event', ...)`, `MutationObserver`,
  `setInterval` listeners registered in `onload` or in a service
  initialised by `main.ts`.

**Cleanup pattern (mandatory in Obsidian plugins):**

- Every `vault.on(...)` MUST have a paired `vault.off(...)` in
  `onunload`.
- Every `register*` call (`registerEvent`, `registerInterval`,
  `registerDomEvent`) is auto-cleaned by the platform; prefer them
  over raw `.on` when possible.
- Every `setInterval` MUST have a `clearInterval` in `onunload`.
- Wrap cleanup in `try/catch` so one failing teardown does not block
  the rest.

## JavaScript (browser or Node, no TypeScript)

**Reachability tooling:**

- `npx eslint --rule 'no-unused-vars: error' --rule 'import/no-unused-modules: error'`.
- `npx depcheck` for unused dependencies.
- `grep -rn "require.*<module>"` and `grep -rn "import.*from.*<module>"`.

**Activation path types:** same as TypeScript. Public-API for
libraries lives in `module.exports` (CommonJS) or named exports
(ESM).

**Cleanup pattern:** same as TypeScript.

## Python

**Reachability tooling:**

- `vulture src/` finds unused functions, classes, and imports. False
  positives on dynamic dispatch happen; whitelist via
  `vulture_whitelist.py`.
- `ruff check --select F401,F811,F841 src/` unused imports,
  redefinitions, unused locals.
- `python -c "import <module>; print([x for x in dir(<module>) if not x.startswith('_')])"`
  for quick public-symbol enumeration.
- AST walker (custom) for `find references to <symbol>` if the
  reference is dynamic (`getattr`, `__call__`, decorator-registered).

**Activation path types:**

- `command` argparse / click / typer subcommand registered in the CLI
  entry point.
- `route` FastAPI / Flask / Django route decorator on a function.
- `endpoint` gRPC service method registered on the server, Celery
  task name registered on the broker.
- `scheduled-job` APScheduler job, Celery beat schedule, Airflow DAG
  task.
- `tool` LangChain tool, OpenAI function-calling tool registered in
  the agent.
- `public-API` exported in `__init__.py` `__all__` list.

**Cleanup pattern:**

Context managers (`with open(...)`, `__enter__`/`__exit__`);
`try/finally` for guaranteed cleanup; `atexit.register(...)` for
process-level cleanup; `weakref.finalize(...)` for object-level
cleanup.

## Go

**Reachability tooling:**

- `staticcheck -checks=U1000 ./...` finds unused functions, variables,
  types.
- `gopls` `find-references` for editor-driven spot checks.
- `go vet ./...` catches unused imports and a few unused-symbol
  patterns.
- `unused -fields ./...` from `honnef.co/go/tools` for field-level
  analysis.

**Activation path types:**

- `command` cobra subcommand registered with `rootCmd.AddCommand(...)`.
- `route` HTTP handler registered on `http.ServeMux`, `chi`, `gin`,
  `echo`.
- `endpoint` gRPC service registered on the server.
- `scheduled-job` ticker-based goroutine started in `main` or a
  service constructor.
- `public-API` exported identifier (Capitalised name) in the package,
  documented at the package level.

**Cleanup pattern:**

`defer` for function-scope cleanup;
`context.WithCancel(...)` plus `<-ctx.Done()` plus `cancel()` for
goroutine teardown; `signal.Notify(...)` for process-level shutdown.

## Rust

**Reachability tooling:**

- `cargo machete` unused dependencies.
- `cargo +nightly udeps` unused dependencies (more thorough).
- `cargo clippy -- -D dead_code` compiler dead-code lint as hard
  error.
- `rust-analyzer` `find references` for editor spot checks.

**Activation path types:**

- `command` clap subcommand registered with `#[derive(Subcommand)]`
  or `App::subcommand(...)`.
- `route` axum / actix / rocket route handler registered in the
  router.
- `endpoint` tonic gRPC service registered on the server.
- `scheduled-job` tokio-cron-scheduler job.
- `public-API` `pub` item in the crate root or in a re-export chain
  leading to the crate root, documented with `///`.

**Cleanup pattern:**

`Drop` impl on types that hold resources (sockets, file handles,
background tasks); scope-end RAII for stack resources;
`tokio::select!` with a cancellation branch for async tasks.

## React (TypeScript or JavaScript application)

**Reachability tooling:**

- `npx eslint-plugin-react/recommended` and
  `eslint-plugin-react-hooks/recommended` flag unused hooks and
  unmounted components.
- `npx ts-prune` (TypeScript projects) exported components never
  imported.
- `grep -rn "<ComponentName" src/` for JSX use spot check.
- Bundle analysers (`webpack-bundle-analyzer`,
  `vite-bundle-visualizer`) reveal which components ship in the
  bundle.

**Activation path types:**

- `route` registered with React Router (Route path/element entry),
  Next.js file-based routing, Remix loaders.
- `UI-element` component mounted in the application tree (find it in
  JSX of a parent that is itself reachable).
- `command` entry in a command-palette component or context-menu
  registry.
- `endpoint` API route under `pages/api/` (Next.js) or `app/api/`
  (Next.js App Router).
- `tool` registered with the framework's agent or AI SDK.
- `public-API` only relevant for component libraries; exported in
  `index.ts`.

**Cleanup pattern:**

`useEffect(() => { ...; return () => { /* cleanup */ }; }, [...])`
the return value is the cleanup function. Mandatory for subscriptions,
intervals, and AbortController-based fetches. `AbortController.abort()`
in the cleanup return for in-flight requests.
`componentWillUnmount` for class components (legacy).

## R

**Reachability tooling:**

- `lintr::lint_package()` with `unused_import_linter()` and
  `object_usage_linter()`.
- `tools::checkUsagePackage(...)` CRAN-grade dead-code report.
- `grep -rn "<function-name>(" R/` for a caller spot check (R is
  permissive about dynamic dispatch; static analysis is partial).

**Activation path types:**

- `endpoint` plumber API route (`#* @get /path`).
- `UI-element` Shiny `output$ID` paired with `IDOutput(...)` in the
  UI (replace `ID` with the output identifier).
- `command` exported function in `NAMESPACE`, callable from a user
  script.
- `scheduled-job` cronR job, RStudio Connect scheduled report.
- `public-API` exported in `NAMESPACE` AND documented with
  `roxygen2` `@export`.

**Cleanup pattern:**

`on.exit(...)` for function-scope cleanup; `withr::with_*` helpers
for scoped state; connection close: `close(con)` paired with
`on.exit(close(con))`.

## Append rows

To add a new stack:

1. Pick the most similar existing entry as a template.
2. Fill the three sections (Reachability tooling, Activation path
   types, Cleanup pattern) in
   `skills/coding/references/reachability-by-stack.md` (the
   authoritative source).
3. Mirror the entry into this docs page.
4. Open a PR titled `feat(coding-ref): add reachability profile for
   STACK_NAME` (replace `STACK_NAME` with your stack).

Out of scope for now: smart-contract stacks (Solidity, Vyper), mobile
native (Swift, Kotlin), embedded (C, C++, Zig). These will be added
on demand when a DIA user works on a project of that class.

## See also

- [Coding guide: Phase 4a Verification Gate](../guides/coding#phase-4a-verification-gate)
- [Requirements Engineering: FEATURE subtype](../guides/requirements-engineering#feature-subtype-since-v320)
- [Drift defense](../concepts/drift-defense): how D9 (spec-level Done
  without runtime evidence) is defended in three layers
- [Consistency Check: Mode A and Mode B](../guides/consistency-check)
