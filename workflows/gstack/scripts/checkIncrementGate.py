#!/usr/bin/env python3
"""Run validator checks and reject progression without fresh passing evidence."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


PLANNING_DOCS = ("brief.md", "contracts.md", "architecture.md", "collaboration.md", "increments.md")
IGNORED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".vitest", ".next", ".turbo"}
ROOT_OUTPUTS = {"dist", "build", "coverage", "playwright-report", "test-results"}
STATUSES = {"pending", "passed", "failed", "blocked"}
SAFE_ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")


class GateError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def within(path, root):
    return path == root or root in path.parents


def strings(value, label, nonempty=False):
    require(isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value), label + " must be a string array")
    require(len(value) == len(set(value)), label + " contains duplicates")
    require(not nonempty or bool(value), label + " must not be empty")
    return value


def criteria_from_brief(path):
    sections = re.findall(r"^## Acceptance criteria\s*\n(.*?)(?=^## |\Z)", path.read_text(), re.M | re.S)
    require(len(sections) == 1, "brief.md needs exactly one '## Acceptance criteria' section")
    criteria = []
    for line in sections[0].splitlines():
        if re.match(r"^\s*\|\s*AC-", line):
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            require(len(columns) == 4 and re.fullmatch(r"AC-[1-9][0-9]*", columns[0]) and all(columns), "Invalid acceptance-criterion row: " + line)
            criteria.append(columns[0])
    return strings(criteria, "Planner acceptance criteria", True)


def check_plan(checks, criteria, label, final=False):
    require(isinstance(checks, list) and bool(checks), label + " needs required checks")
    ids, covered = set(), set()
    for check in checks:
        require(isinstance(check, dict), label + " check must be an object")
        cid = check.get("id")
        require(isinstance(cid, str) and SAFE_ID.fullmatch(cid) and cid not in ids, label + " has invalid/duplicate check ID")
        ids.add(cid)
        argv = check.get("argv")
        require(isinstance(argv, list) and bool(argv) and all(isinstance(arg, str) and arg for arg in argv), label + " argv must be a nonempty argument array")
        mapped = strings(check.get("criteria"), label + " check criteria")
        require(set(mapped) <= set(criteria), label + " check refers to unknown criteria")
        require(check.get("kind") in {"behavior", "auxiliary"}, label + " kind must be behavior or auxiliary")
        require(check.get("scope") in {"isolated", "integrated"}, label + " scope must be isolated or integrated")
        strings(check.get("testFiles"), label + " testFiles", check["kind"] == "behavior")
        require(isinstance(check.get("cwd", "."), str) and bool(check.get("cwd", ".")), label + " cwd must be a path")
        timeout = check.get("timeoutSeconds", 300)
        require(type(timeout) is int and timeout > 0, label + " timeoutSeconds must be positive")
        if check["kind"] == "behavior" and (not final or check["scope"] == "integrated"):
            covered.update(mapped)
        if check["kind"] == "auxiliary":
            require(not mapped, "Build/lint checks cannot claim acceptance coverage")
    require(any(check["kind"] == "behavior" for check in checks), label + " needs a behavioral test")
    require(covered == set(criteria), label + " lacks behavioral coverage for " + ", ".join(sorted(set(criteria) - covered)))


def load_state(path):
    state = json.loads(path.read_text())
    require(isinstance(state, dict) and type(state.get("schemaVersion")) is int and state["schemaVersion"] == 1, "Unsupported validation-state schema")
    require(isinstance(state.get("sourcePath"), str) and state["sourcePath"], "sourcePath is required")
    source = (path.parent / state["sourcePath"]).resolve()
    require(source.is_dir() and source != path.parent, "sourcePath must be an existing source directory separate from the document directory")
    for name in PLANNING_DOCS:
        require((path.parent / name).is_file(), "Missing planning document: " + name)
    criteria = strings(state.get("acceptanceCriteria"), "acceptanceCriteria", True)
    require(set(criteria) == set(criteria_from_brief(path.parent / "brief.md")), "State criteria do not match planner's brief")
    increments = state.get("increments")
    require(isinstance(increments, list) and bool(increments), "increments must not be empty")
    seen, mapped = set(), set()
    for inc in increments:
        require(isinstance(inc, dict), "Increment must be an object")
        iid = inc.get("id")
        require(isinstance(iid, str) and SAFE_ID.fullmatch(iid) and iid != "final" and iid not in seen, "Invalid/duplicate increment ID")
        deps = strings(inc.get("dependsOn"), iid + " dependsOn")
        require(set(deps) <= seen, iid + " dependencies must refer to earlier increments")
        assigned = strings(inc.get("criteria"), iid + " criteria")
        require(set(assigned) <= set(criteria), iid + " has unknown criteria")
        mapped.update(assigned)
        check_plan(inc.get("checks"), assigned, iid)
        seen.add(iid)
    require(mapped == set(criteria), "Every planner criterion must be assigned to an increment")
    require(isinstance(state.get("final"), dict), "final validation is required")
    check_plan(state["final"].get("checks"), criteria, "final", True)
    for entry in increments + [state["final"]]:
        require(entry.get("status", "pending") in STATUSES, "Unknown validation status")
        require(type(entry.get("correctionPassesUsed", 0)) is int and 0 <= entry.get("correctionPassesUsed", 0) <= 2, "Invalid correction count")
        require(isinstance(entry.get("attempts", []), list) and all(isinstance(a, dict) for a in entry.get("attempts", [])), "Invalid validation history")
    return state, source


def snapshot(state, source, documents):
    files = []
    def walk_error(error):
        raise GateError("Cannot fingerprint source: " + str(error))

    def keep_directory(folder, name):
        if name in IGNORED_DIRS or (folder == source and name in ROOT_OUTPUTS):
            return False
        return not (within(documents, source) and within((folder / name).resolve(), documents))

    for current, dirs, names in os.walk(str(source), followlinks=False, onerror=walk_error):
        folder = Path(current)
        dirs[:] = sorted(name for name in dirs if keep_directory(folder, name))
        for name in dirs:
            require(not (folder / name).is_symlink(), "Source directory symlinks are unsupported: " + str(folder / name))
        for name in sorted(names):
            if name == ".DS_Store":
                continue
            item = folder / name
            require(within(item.resolve(), source), "Source symlink escapes sourcePath: " + str(item))
            require(item.is_file(), "Unsupported source file: " + str(item))
            files.append([str(item.relative_to(source)), digest(item), item.stat().st_mode & 0o111, os.readlink(str(item)) if item.is_symlink() else None])
    plan = {"schemaVersion": state["schemaVersion"], "sourcePath": str(source), "acceptanceCriteria": state["acceptanceCriteria"], "increments": [{key: value for key, value in inc.items() if key not in {"status", "attempts", "correctionPassesUsed"}} for inc in state["increments"]], "finalChecks": state["final"]["checks"]}
    docs = {name: digest(documents / name) for name in PLANNING_DOCS}
    for name in ("handoff.md", "communications.md"):
        docs[name] = digest(documents / name) if (documents / name).is_file() else None
    return {"sourceSha256": json_digest(files), "documentSha256": docs, "planSha256": json_digest(plan), "gateSha256": digest(Path(__file__))}


def fresh_pass(entry, current, documents, label):
    require(entry.get("status") == "passed", label + " has not passed validation")
    attempts = entry.get("attempts", [])
    require(bool(attempts), label + " has no validation evidence")
    attempt = attempts[-1]
    require(attempt.get("verdict") == "passed" and attempt.get("reviewed") is True, label + " lacks validator review")
    require(attempt.get("snapshot") == current, label + " evidence is stale; rerun validation")
    results = attempt.get("results")
    require(isinstance(results, list) and len(results) == len(entry["checks"]), label + " has incomplete check results")
    for check, result in zip(entry["checks"], results):
        require(isinstance(result, dict) and result.get("id") == check["id"] and result.get("status") == "passed" and result.get("exitCode") == 0 and result.get("argv") == check["argv"], label + " has invalid check evidence")
        log = result.get("log")
        require(isinstance(log, str), label + " is missing a test log")
        log_path = (documents / log).resolve()
        require(within(log_path, documents) and log_path.is_file() and digest(log_path) == result.get("logSha256"), label + " test log is missing or changed")


def select(state, iid):
    for index, inc in enumerate(state["increments"]):
        if inc["id"] == iid:
            return index, inc
    raise GateError("Unknown increment: " + iid)


def gate(state, current, documents, iid=None):
    final = state["final"]
    unresolved_failure = any(attempt.get("verdict") == "failed" for attempt in failures_since_pass(final))
    require(not (unresolved_failure and final.get("correctionPassesUsed", 0) >= 2), "Final validation exhausted its correction allowance")
    index, target = select(state, iid) if iid else (len(state["increments"]), state["final"])
    for previous in state["increments"][:index]:
        fresh_pass(previous, current, documents, previous["id"])
    if iid:
        require(not (target.get("status") == "failed" and target.get("correctionPassesUsed", 0) >= 2), iid + " exhausted its correction allowance")
    else:
        fresh_pass(target, current, documents, "final")


def save(path, state):
    fd, temp = tempfile.mkstemp(prefix=".validationState-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(state, stream, indent=2)
            stream.write("\n")
        os.replace(temp, str(path))
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def failures_since_pass(entry):
    failures = []
    for attempt in reversed(entry.get("attempts", [])):
        if attempt.get("verdict") == "passed":
            break
        if attempt.get("verdict") == "failed":
            failures.append(attempt)
    return failures


def run_check(check, source, documents, label, number):
    log_dir = documents / "validationLogs"
    log_dir.mkdir(exist_ok=True)
    require(not log_dir.is_symlink(), "validationLogs must not be a symlink")
    log = log_dir / (label + "-" + str(number) + "-" + check["id"] + ".log")
    require(not log.is_symlink() and not log.exists(), "Validation log already exists: " + str(log))
    cwd = (source / check.get("cwd", ".")).resolve()
    result = {"id": check["id"], "argv": check["argv"], "cwd": str(cwd), "status": "blocked", "exitCode": None, "log": str(log.relative_to(documents))}
    with log.open("x") as output:
        try:
            require(within(cwd, source) and cwd.is_dir(), "Check working directory must exist inside sourcePath")
            for name in check["testFiles"]:
                file_path = (source / name).resolve()
                require(within(file_path, source) and file_path.is_file(), "Missing test file: " + name)
            process = subprocess.Popen(check["argv"], cwd=str(cwd), stdout=output, stderr=subprocess.STDOUT, shell=False, start_new_session=os.name == "posix")
            try:
                code = process.wait(timeout=check.get("timeoutSeconds", 300))
            finally:
                if process.poll() is None:
                    if os.name == "posix":
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                    process.wait()
            result.update(exitCode=code, status="passed" if code == 0 else "failed")
        except (GateError, OSError, subprocess.TimeoutExpired) as error:
            output.write("\nBLOCKED: " + str(error) + "\n")
    result["logSha256"] = digest(log)
    return result


def validate_entry(state, entry, source, path, label, reviewed, correction):
    before = snapshot(state, source, path.parent)
    attempts = entry.setdefault("attempts", [])
    failures = failures_since_pass(entry)
    changed_failure = failures and failures[0].get("snapshot") != before
    require(not (failures and entry.get("correctionPassesUsed", 0) >= 2), label + " exhausted its correction allowance")
    require(not changed_failure or correction, label + " changed after failure; specify --correction " + label)
    if correction:
        require(entry.get("correctionPassesUsed", 0) < 2, label + " exhausted its correction allowance")
        entry["correctionPassesUsed"] = entry.get("correctionPassesUsed", 0) + 1
    number = len(attempts) + 1
    record = {"number": number, "at": datetime.now(timezone.utc).isoformat(), "snapshot": before, "reviewed": reviewed, "correction": correction, "verdict": "blocked", "results": []}
    attempts.append(record)
    entry["status"] = "blocked"
    if label != "final":
        state["final"]["status"] = "pending"
    # Persist a blocked attempt before executing side effects, including crashes.
    save(path, state)
    require((path.parent / "handoff.md").is_file(), "Validator needs handoff.md before running checks")
    for check in entry["checks"]:
        result = run_check(check, source, path.parent, label, number)
        record["results"].append(result)
        save(path, state)
    outcomes = [result["status"] for result in record["results"]]
    record["verdict"] = "failed" if "failed" in outcomes else "blocked" if "blocked" in outcomes else "passed"
    try:
        require(snapshot(state, source, path.parent) == before, "Source or planning documents changed during validation")
    except (GateError, OSError) as error:
        record["verdict"] = "blocked"
        record["reason"] = str(error)
    entry["status"] = record["verdict"]
    save(path, state)
    print(label + ": " + record["verdict"] + " (attempt " + str(number) + ")")
    require(record["verdict"] == "passed", label + " validation did not pass; inspect validationLogs and record issues in validation.md")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Read-only gate before implementation, or completion")
    validate = sub.add_parser("validate", help="Validator-only: execute required suites and record evidence")
    for command in (check, validate):
        command.add_argument("--state", type=Path, required=True)
        target = command.add_mutually_exclusive_group(required=True)
        target.add_argument("--increment" if command is check else "--through")
        target.add_argument("--final", action="store_true")
    validate.add_argument("--reviewed", action="store_true", help="Attest that criteria, assertions, handoffs, and supplemental checks were reviewed")
    validate.add_argument("--correction", action="append", default=[], help="Increment ID or final whose correction pass this run consumes")
    args = parser.parse_args(argv)
    path = args.state.resolve()
    lock = path.parent / ".validationGate.lock"
    acquired = False
    try:
        if args.command == "validate":
            require(args.reviewed, "Only validator runs validate after review; --reviewed is required")
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            acquired = True
            with os.fdopen(fd, "w") as stream:
                stream.write(str(os.getpid()) + "\n")
        else:
            require(not lock.exists(), "Validation is in progress or a stale .validationGate.lock needs inspection")
        state, source = load_state(path)
        current = snapshot(state, source, path.parent)
        if args.command == "check":
            gate(state, current, path.parent, args.increment)
            print("ALLOW: " + (args.increment or "application completion"))
        else:
            end = select(state, args.through)[0] + 1 if args.through else len(state["increments"])
            labels = [inc["id"] for inc in state["increments"][:end]] + (["final"] if args.final else [])
            strings(args.correction, "--correction")
            require(set(args.correction) <= set(labels), "Correction refers to a target outside this validation run")
            for inc in state["increments"][:end]:
                gate(state, snapshot(state, source, path.parent), path.parent, inc["id"])
                validate_entry(state, inc, source, path, inc["id"], args.reviewed, inc["id"] in args.correction)
            if args.final:
                validate_entry(state, state["final"], source, path, "final", args.reviewed, "final" in args.correction)
            # Verify the entire prefix remains fresh after the last suite.
            current = snapshot(state, source, path.parent)
            for inc in state["increments"][:end]:
                fresh_pass(inc, current, path.parent, inc["id"])
            if args.final:
                gate(state, current, path.parent)
        return 0
    except (GateError, OSError, ValueError, TypeError, KeyError) as error:
        print("DENY: " + str(error), file=sys.stderr)
        return 1
    finally:
        if acquired:
            lock.unlink()


if __name__ == "__main__":
    sys.exit(main())
