# Increment validation gate

Run [scripts/checkIncrementGate.py](scripts/checkIncrementGate.py) from the repository root with Python 3.8 or newer. It uses only the standard library. The application supplies its own testing libraries and commands.

## Set up the application record

Architect creates `outputs/gstack/<applicationName>/validationState.json` from [validationStateTemplate.json](validationStateTemplate.json) after planner confirms the increment assignments. Replace the example with the application's actual AC-IDs, ordered increments, test files, and commands. Planner owns criterion changes; architect owns test-plan changes; validator owns recorded verdicts and attempts.

- `sourcePath` is resolved relative to the JSON file, including for existing apps. Absolute source paths are also allowed. Source must be an existing directory separate from the document directory.
- Keep `brief.md`, `architecture.md`, `contracts.md`, `collaboration.md`, and `increments.md` beside the state file. Planner's criteria use the table in [acceptanceTestTemplate.md](acceptanceTestTemplate.md).
- `acceptanceCriteria` must exactly match the planner table. Every criterion must be assigned to at least one increment and mapped to a behavioral check. Dependencies must point to earlier increments. All earlier increments must pass before a later one starts, even if they are not listed as direct dependencies.
- Each increment needs a behavioral check, including setup increments without AC-IDs. `testFiles` are concrete source-root-relative paths; `cwd` is a working directory inside source. `argv` is an argument array, executed without an implicit shell. Use installed, finite, non-watch test commands and designated test services. Default timeout is 300 seconds per command.
- `kind: behavior` can claim criterion coverage; `kind: auxiliary` is for build/lint/type checks and must have no criterion IDs. `scope: isolated` describes test-double evidence. Final checks must cover every criterion with `scope: integrated`, using the actual boundaries required by that criterion. Validator verifies these declarations against the assertions and actual run.
- Preserve `attempts` and `correctionPassesUsed` when revising plans. Never reset history to bypass a failed gate. Do not manually set a passing status.

`validationState.json` is authoritative for execution verdicts, counts, and command evidence. `increments.md` remains the human-readable plan; `validation.md` records validator findings, manual evidence, and links to JSON attempts/logs. Do not duplicate live statuses in planning documents. Changes to those planning documents intentionally invalidate prior evidence.

## Before starting or correcting an increment

```sh
python3 workflows/gstack/scripts/checkIncrementGate.py check \
  --state outputs/gstack/myApp/validationState.json --increment I-2
```

Exit `0` prints `ALLOW`; any nonzero exit denies progression. Orchestrator or increment owner runs this immediately before the first contribution to an increment or correction pass. Contributors confirm that successful entry check, then work within the same goal; they do not repeat entry checks between file edits or sequential contributions. `check` is read-only and does not run tests. A runner must use its exit code as the dispatch condition; this script does not intercept unrelated editor or shell operations.

## Validator runs acceptance tests after every increment

Validator first reviews criterion assertions, test collection, required handoff acknowledgements, and supplemental manual checks. Record that review in `validation.md`; `--reviewed` attests it is complete. Builder self-checks are not authoritative. Put setup and run instructions in `handoff.md` before validation.

```sh
python3 workflows/gstack/scripts/checkIncrementGate.py validate \
  --state outputs/gstack/myApp/validationState.json --through I-1 --reviewed
```

This reruns every earlier increment through the selected one, in order, and stops at the first failed or blocked increment. Each attempt saves executed arguments, working directories, exit codes, log paths and hashes, and source/planning fingerprints. The validator must still inspect library reports: exit zero alone cannot prove that meaningful assertions ran or that no required cases were skipped. Configure suites to reject zero collected acceptance tests; never enable options that allow empty suites to pass.

After correcting a failed increment, consume its correction pass explicitly:

```sh
python3 workflows/gstack/scripts/checkIncrementGate.py validate \
  --state outputs/gstack/myApp/validationState.json --through I-2 --reviewed \
  --correction I-2
```

The gate requires a correction flag when the source or plan changed after a failed verdict and enforces the two-pass limit. Read-only rechecks and prerequisite recovery do not consume a correction pass. When a final failure also required corrections, include `--correction final` in the final run as well as flags for corrected increments. Do not start fixes after the applicable allowance is exhausted.

## Final validation and completion

```sh
python3 workflows/gstack/scripts/checkIncrementGate.py validate \
  --state outputs/gstack/myApp/validationState.json --final --reviewed
python3 workflows/gstack/scripts/checkIncrementGate.py check \
  --state outputs/gstack/myApp/validationState.json --final
```

Final validation reruns all increments, then the final integrated suites. Completion requires the final gate as well as validator's criterion, contract, manual-check, and reproducible-setup review. An increment pass is not a final verdict.

## Freshness and limits

Fingerprints include the full source tree, including uncommitted/untracked source, tests, configuration, and lockfiles; all five planning documents; optional handoff and communication documents; the JSON test plan; and the gate implementation. Contract version is the SHA-256 of `contracts.md`. State/history fields, validator narrative, and logs are excluded so recording evidence does not invalidate itself. A deleted, added, renamed, edited, or executable-mode-changed source file invalidates evidence.

Dependency/cache directories (`.git`, `node_modules`, `.venv`, `venv`, `__pycache__`, `.pytest_cache`, `.vitest`, `.next`, `.turbo`) and root generated outputs (`dist`, `build`, `coverage`, `playwright-report`, `test-results`) are excluded, as is `.DS_Store`. Never put authored code, tests, or authoritative configuration in these directories. If documents are nested under an existing source root, that document subtree is excluded from source hashing and its required files are hashed separately. Directory symlinks and file symlinks outside source are rejected rather than silently ignoring external dependencies.

Any application change requires rerunning the earlier prefix. This conservative policy avoids guessing which tests are affected. Changes during a validation attempt block its verdict. External database/service state and installed dependency contents are not fingerprinted: use reproducible fixtures, lockfiles, and recorded prerequisites, and rerun validation when those environments change.

Missing tools/test files or timeouts are blocked; nonzero test exits are failed. Failed or blocked records, missing/altered logs, stale snapshots, invalid plans, omitted criteria, and unknown increment IDs deny advancement. Commands run with the caller's permissions; the gate is not a sandbox or proof against deliberately forged records. Human review and role ownership remain workflow requirements.

Validation writes state atomically and uses `.validationGate.lock` to exclude concurrent validation. If a process is killed, inspect its blocked attempt and PID in the lock, confirm it is no longer running, and remove only the stale lock before retrying. Preserve its logs and history. Keep test output free of credentials.

## Test the gate itself

```sh
python3 -m unittest discover -s workflows/gstack/scripts/tests -p 'test*.py'
```
