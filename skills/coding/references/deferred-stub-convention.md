# Deferred-stub marker convention (binding)

A stub implementation is any code that intentionally returns a no-op,
empty result, or hard-coded placeholder while waiting on later wiring,
external data, an upstream feature, or a real implementation in a
later phase. Stubs are normal in iterative development; what is
forbidden is silent stubs.

**Every stub MUST carry a `FIXME(stub):` marker AND a paired
`FIX-{ee}-{ff}-{nn}` row in the backlog.** The two are bidirectionally
bound: each marker references its FIX-ID, each FIX row that documents
a stub references at least one source location.

Marker syntax (per-language comment style, identical content):

```
// FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
# FIXME(stub): <one-line reason> -- see FIX-{ee}-{ff}-{nn}
```

Use `//` for C-family languages (TypeScript, JavaScript, Java, Go,
Rust, C#, Swift, Kotlin). Use `#` for Python, Ruby, R, shell scripts.

The FIX row in `_devprocess/context/BACKLOG.md` and its detail file
carry the context: why the stub is there, what unblocks it, what to
do when it is unblocked.

**`/consistency-check` Mode A enforces the binding (E-13):**

- Every `FIXME(stub):` in the source tree must reference an open FIX
  row by ID; missing or unresolved IDs surface as
  `stub-without-fix-row` findings.
- Every FIX row whose notes contain `Wiring offen`, `stub`, or similar
  deferral language must reference at least one source location;
  missing references surface as `fix-without-stub-evidence` findings.

**Why bidirectional.** A marker without a FIX row is invisible at the
backlog level; nobody plans to remove it. A FIX row without a marker
is stale paperwork; nobody can find the actual code to remove. The
bidirectional binding turns silent deferrals into auditable items.
