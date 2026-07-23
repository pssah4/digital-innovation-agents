#!/usr/bin/env node
// ReDoS probe -- isolated, opt-in dynamic verification of ONE suspect regex.
//
// This does NOT run the audited application. It takes a single regex source
// (flagged by the SAST scan) plus a "pump" string and measures whether that
// regex exhibits catastrophic backtracking. The suspect regex is executed
// inside a worker_thread with a hard deadline; the main thread stays
// responsive and terminates the worker if it blows the deadline. No network,
// no filesystem writes outside argv, no eval of arbitrary code -- only
// `new RegExp(source, flags)` on the provided pattern.
//
// The pump string is `pumpChar * pumpLen + pumpSuffix`. The suffix matters:
// catastrophic backtracking usually needs input that ALMOST matches and then
// fails, so a non-matching trailing character forces the engine to explore
// the exponential search space. The default suffix "!" achieves that for the
// classic nested-quantifier patterns; override it for a specific attack shape.
//
// Usage:
//   node redos_probe.mjs --pattern '(a+)+$' [--flags ''] [--pump-char a]
//                        [--pump-len 40] [--pump-suffix '!'] [--deadline-ms 500]
//   node redos_probe.mjs --json '{"pattern":"(a+)+$","pumpLen":40}'
//
// Output (stdout, JSON):
//   {"hangs": true|false, "elapsed_ms": N, "deadline_ms": D,
//    "pattern": "...", "pump_len": N, "error": null|"..."}
// Exit: 0 = measured (hang or not), 2 = usage/setup error.

import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';

// ---- worker side: run the suspect regex, report elapsed ----
if (!isMainThread) {
  const { pattern, flags, pump } = workerData;
  const start = process.hrtime.bigint();
  let error = null;
  try {
    const re = new RegExp(pattern, flags);
    // The potentially catastrophic operation. If it backtracks forever the
    // main thread's timer terminates this worker; we never get here.
    re.test(pump);
  } catch (e) {
    error = String(e && e.message ? e.message : e);
  }
  const elapsed = Number(process.hrtime.bigint() - start) / 1e6;
  parentPort.postMessage({ elapsed_ms: elapsed, error });
  // fall through: worker exits naturally
}

// ---- main side: parse args, spawn worker, enforce deadline ----
else {
  const args = parseArgs(process.argv.slice(2));

  const pattern = args.pattern;
  if (!pattern) {
    process.stdout.write(JSON.stringify({
      error: "no --pattern (or --json {pattern}) given", hangs: null,
    }) + "\n");
    process.exit(2);
  }
  const flags = args.flags ?? "";
  const pumpChar = (args.pumpChar ?? "a").slice(0, 1) || "a";
  const pumpLen = clampInt(args.pumpLen, 1, 100000, 40);
  const pumpSuffix = args.pumpSuffix ?? "!";
  const deadlineMs = clampInt(args.deadlineMs, 10, 60000, 500);
  const pump = pumpChar.repeat(pumpLen) + pumpSuffix;

  const result = {
    hangs: false,
    elapsed_ms: 0,
    deadline_ms: deadlineMs,
    pattern,
    pump_len: pumpLen,
    error: null,
  };

  let settled = false;
  const worker = new Worker(new URL(import.meta.url), {
    workerData: { pattern, flags, pump },
  });

  const timer = setTimeout(() => {
    if (settled) return;
    settled = true;
    result.hangs = true;
    result.elapsed_ms = deadlineMs;
    result.error = null;
    worker.terminate().finally(() => finish(result));
  }, deadlineMs);

  worker.on("message", (msg) => {
    if (settled) return;
    settled = true;
    clearTimeout(timer);
    result.hangs = false;
    result.elapsed_ms = Math.round((msg.elapsed_ms + Number.EPSILON) * 100) / 100;
    result.error = msg.error ?? null;
    finish(result);
  });

  worker.on("error", (err) => {
    if (settled) return;
    settled = true;
    clearTimeout(timer);
    result.error = String(err && err.message ? err.message : err);
    finish(result);
  });
}

function finish(result) {
  process.stdout.write(JSON.stringify(result) + "\n");
  process.exit(0);
}

function parseArgs(argv) {
  // Support --json '{...}' as a single-object form, plus --key value flags.
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") {
      try {
        const obj = JSON.parse(argv[++i] ?? "{}");
        if (obj.pattern != null) out.pattern = String(obj.pattern);
        if (obj.flags != null) out.flags = String(obj.flags);
        if (obj.pumpChar != null) out.pumpChar = String(obj.pumpChar);
        if (obj.pumpLen != null) out.pumpLen = obj.pumpLen;
        if (obj.pumpSuffix != null) out.pumpSuffix = String(obj.pumpSuffix);
        if (obj.deadlineMs != null) out.deadlineMs = obj.deadlineMs;
      } catch {
        // ignore malformed --json; validation happens on pattern presence
      }
      continue;
    }
    if (a === "--pattern") out.pattern = argv[++i];
    else if (a === "--flags") out.flags = argv[++i];
    else if (a === "--pump-char") out.pumpChar = argv[++i];
    else if (a === "--pump-len") out.pumpLen = argv[++i];
    else if (a === "--pump-suffix") out.pumpSuffix = argv[++i];
    else if (a === "--deadline-ms") out.deadlineMs = argv[++i];
  }
  return out;
}

function clampInt(v, lo, hi, dflt) {
  const n = parseInt(v, 10);
  if (Number.isNaN(n)) return dflt;
  return Math.max(lo, Math.min(hi, n));
}
