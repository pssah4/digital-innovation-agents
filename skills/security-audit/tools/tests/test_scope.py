"""Tests for security-audit/tools/lib/scope.py.

Builds a throwaway git repo in a temp dir, exercises each scope
category against real git history. Assertion-based, pytest-discoverable.

    python3 skills/security-audit/tools/tests/test_scope.py
"""
from __future__ import annotations
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path


LIB_DIR = Path(__file__).resolve().parents[1] / "lib"


def _load(module_name: str):
    path = LIB_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"sa_{module_name}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[f"sa_{module_name}"] = mod
    spec.loader.exec_module(mod)
    return mod


def _run(args, cwd):
    subprocess.run(args, cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _commit(tmp: Path, name: str, content: str, msg: str) -> None:
    (tmp / name).write_text(content, encoding="utf-8")
    _run(["git", "add", "-A"], tmp)
    _run(["git", "commit", "-q", "-m", msg], tmp)


def _init_repo(tmp: Path) -> None:
    _run(["git", "init", "-q", "-b", "main"], tmp)
    _run(["git", "config", "user.email", "t@t.t"], tmp)
    _run(["git", "config", "user.name", "t"], tmp)


def test_scope_full_lists_all_tracked() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "console.log(1)\n", "a")
        _commit(tmp, "b.ts", "console.log(2)\n", "b")
        r = m.resolve_scope(tmp, "full")
        assert set(r.files) == {"a.ts", "b.ts"}, r.files
        assert r.scope == "full"
        print("OK: full lists all tracked files")


def test_scope_commit_lists_last_commit_only() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "1\n", "a")
        _commit(tmp, "b.ts", "2\n", "b")
        r = m.resolve_scope(tmp, "commit")
        assert r.files == ["b.ts"], r.files
        print("OK: commit lists last commit only")


def test_scope_working_lists_uncommitted() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "1\n", "a")
        # modify tracked + add untracked, do not commit
        (tmp / "a.ts").write_text("1\n2\n", encoding="utf-8")
        (tmp / "new.ts").write_text("x\n", encoding="utf-8")
        r = m.resolve_scope(tmp, "working")
        assert set(r.files) == {"a.ts", "new.ts"}, r.files
        print("OK: working lists uncommitted (modified + untracked)")


def test_scope_staged_lists_only_staged() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "1\n", "a")
        (tmp / "a.ts").write_text("1\n2\n", encoding="utf-8")
        (tmp / "staged.ts").write_text("s\n", encoding="utf-8")
        _run(["git", "add", "staged.ts"], tmp)  # only this one staged
        r = m.resolve_scope(tmp, "staged")
        assert r.files == ["staged.ts"], r.files
        print("OK: staged lists only staged files")


def test_scope_branch_uses_merge_base() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "base.ts", "0\n", "base")
        _run(["git", "checkout", "-q", "-b", "feature"], tmp)
        _commit(tmp, "feat1.ts", "1\n", "f1")
        _commit(tmp, "feat2.ts", "2\n", "f2")
        r = m.resolve_scope(tmp, "branch", base="main")
        assert set(r.files) == {"feat1.ts", "feat2.ts"}, r.files
        assert "base.ts" not in r.files
        print("OK: branch uses merge-base against main")


def test_scope_range_between_two_commits() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "1\n", "a")
        first = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=tmp, text=True).strip()
        _commit(tmp, "b.ts", "2\n", "b")
        _commit(tmp, "c.ts", "3\n", "c")
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=tmp, text=True).strip()
        r = m.resolve_scope(tmp, "range", rng=f"{first}..{head}")
        assert set(r.files) == {"b.ts", "c.ts"}, r.files
        print("OK: range between two commits")


def test_diff_scope_filters_deleted_and_nonexistent() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "1\n", "a")
        _commit(tmp, "b.ts", "2\n", "b")
        # last commit deletes a.ts
        _run(["git", "rm", "-q", "a.ts"], tmp)
        _run(["git", "commit", "-q", "-m", "del a"], tmp)
        r = m.resolve_scope(tmp, "commit")
        # a.ts is gone from the tree -> must not be handed to a scanner.
        assert "a.ts" not in r.files, r.files
        print("OK: diff scope filters deleted files")


def test_unknown_scope_raises() -> None:
    m = _load("scope")
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        _init_repo(tmp)
        _commit(tmp, "a.ts", "1\n", "a")
        try:
            m.resolve_scope(tmp, "bogus")
        except ValueError:
            print("OK: unknown scope raises ValueError")
            return
        assert False, "expected ValueError for unknown scope"


ALL_TESTS = [
    test_scope_full_lists_all_tracked,
    test_scope_commit_lists_last_commit_only,
    test_scope_working_lists_uncommitted,
    test_scope_staged_lists_only_staged,
    test_scope_branch_uses_merge_base,
    test_scope_range_between_two_commits,
    test_diff_scope_filters_deleted_and_nonexistent,
    test_unknown_scope_raises,
]


def main() -> int:
    failed = 0
    for t in ALL_TESTS:
        try:
            t()
        except AssertionError as exc:
            print(f"FAIL: {t.__name__}: {exc}", file=sys.stderr)
            failed += 1
        except Exception as exc:  # noqa: BLE001 - surface unexpected errors
            print(f"ERROR: {t.__name__}: {exc!r}", file=sys.stderr)
            failed += 1
    if failed:
        print(f"\n{failed} test(s) failed.", file=sys.stderr)
        return 1
    print("\nAll scope tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
