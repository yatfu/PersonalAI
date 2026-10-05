"""Black-box tests using real acceptance-test subprocesses and temporary apps."""

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "checkIncrementGate.py"


class IncrementGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.docs = Path(self.temp.name)
        self.app = self.docs / "app"
        self.app.mkdir()
        (self.app / "behavior.py").write_text("def add(a, b):\n    return a + b\n\ndef valid_title(title):\n    return bool(title.strip())\n")
        (self.app / "acceptanceTests.py").write_text(
            "import unittest\nfrom behavior import add, valid_title\n"
            "class AcceptanceTests(unittest.TestCase):\n"
            "    def testAC1(self):\n        self.assertEqual(add(2, 3), 5)\n"
            "    def testAC2(self):\n        self.assertFalse(valid_title('   '))\n"
        )
        (self.docs / "brief.md").write_text(
            "# Brief\n\n## Acceptance criteria\n\n"
            "| ID | Given | When | Then |\n|---|---|---|---|\n"
            "| AC-1 | Two numbers | Added | Their sum is returned |\n"
            "| AC-2 | Blank title | Validated | It is rejected |\n"
        )
        for name in ("contracts.md", "architecture.md", "collaboration.md", "increments.md", "handoff.md"):
            (self.docs / name).write_text("# " + name + "\n")
        self.path = self.docs / "validationState.json"
        checks = [self.make_check("T-1", "AC-1", "testAC1"), self.make_check("T-2", "AC-2", "testAC2")]
        self.state = {
            "schemaVersion": 1, "sourcePath": "app", "acceptanceCriteria": ["AC-1", "AC-2"],
            "increments": [
                {"id": "I-1", "dependsOn": [], "criteria": ["AC-1"], "checks": [checks[0]]},
                {"id": "I-2", "dependsOn": ["I-1"], "criteria": ["AC-2"], "checks": [checks[1]]},
            ],
            "final": {"checks": copy.deepcopy(checks)},
        }
        self.write()

    def make_check(self, cid, criterion, case):
        return {"id": cid, "criteria": [criterion], "kind": "behavior", "scope": "integrated", "testFiles": ["acceptanceTests.py"], "argv": [sys.executable, "-B", "-m", "unittest", "acceptanceTests.AcceptanceTests." + case]}

    def write(self):
        self.path.write_text(json.dumps(self.state))

    def read(self):
        self.state = json.loads(self.path.read_text())
        return self.state

    def cli(self, command, *args, success=True):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), command, "--state", str(self.path)] + list(args), capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("DENY:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        return result

    def validate(self, through="I-1", *args, success=True):
        return self.cli("validate", "--through", through, "--reviewed", *args, success=success)

    def test_order_and_read_only_checks(self):
        before = self.path.read_bytes()
        self.cli("check", "--increment", "I-1")
        self.cli("check", "--increment", "I-2", success=False)
        self.assertEqual(before, self.path.read_bytes())
        self.validate()
        self.cli("check", "--increment", "I-2")
        self.assertEqual(self.read()["increments"][0]["attempts"][-1]["results"][0]["exitCode"], 0)

    def test_review_is_required(self):
        self.cli("validate", "--through", "I-1", success=False)
        self.assertFalse((self.docs / "validationLogs").exists())

    def test_failed_behavior_blocks_progression(self):
        (self.app / "behavior.py").write_text("def add(a, b): return 0\ndef valid_title(title): return False\n")
        self.validate(success=False)
        self.assertEqual(self.read()["increments"][0]["status"], "failed")
        self.cli("check", "--increment", "I-2", success=False)

    def test_missing_tool_and_test_file_are_blocked(self):
        self.state["increments"][0]["checks"][0]["argv"] = ["gstack-nonexistent-executable"]
        self.write()
        self.validate(success=False)
        self.assertEqual(self.read()["increments"][0]["status"], "blocked")
        self.state["increments"][0]["checks"][0]["testFiles"] = ["missing.test.py"]
        self.write()
        self.validate(success=False)
        self.assertEqual(self.read()["increments"][0]["status"], "blocked")

    def test_future_tests_can_be_created_in_their_own_increment(self):
        self.state["increments"][1]["checks"][0]["testFiles"] = ["future.test.py"]
        self.write()
        self.validate()
        self.cli("check", "--increment", "I-2")
        self.validate("I-2", success=False)
        self.assertEqual(self.read()["increments"][1]["status"], "blocked")

    def test_source_add_edit_delete_and_mode_changes_invalidate(self):
        self.validate()
        original = (self.app / "behavior.py").read_text()
        (self.app / "behavior.py").write_text(original + "# changed\n")
        self.cli("check", "--increment", "I-2", success=False)
        self.validate()
        added = self.app / "newFile.py"
        added.write_text("# new\n")
        self.cli("check", "--increment", "I-2", success=False)
        self.validate()
        added.unlink()
        self.cli("check", "--increment", "I-2", success=False)
        self.validate()
        os.chmod(str(self.app / "behavior.py"), 0o755)
        self.cli("check", "--increment", "I-2", success=False)

    def test_contract_and_test_plan_changes_invalidate(self):
        self.validate()
        (self.docs / "contracts.md").write_text("# Changed contract\n")
        self.cli("check", "--increment", "I-2", success=False)
        self.validate()
        self.read()["increments"][0]["checks"][0]["timeoutSeconds"] = 100
        self.write()
        self.cli("check", "--increment", "I-2", success=False)

    def test_nested_source_and_test_files_are_fingerprinted(self):
        for directory in ("src/features", "tests/integration"):
            folder = self.app / directory
            folder.mkdir(parents=True)
            file = folder / "nested.py"
            file.write_text("# initial\n")
            self.validate()
            file.write_text("# changed\n")
            self.cli("check", "--increment", "I-2", success=False)

    def test_existing_app_can_contain_its_document_directory(self):
        self.state["sourcePath"] = "."
        self.write()
        self.cli("check", "--increment", "I-1", success=False)
        # A source root may be an ancestor of documents, but not the same directory.
        outer = self.docs / "project"
        outer.mkdir()
        documents = outer / "workflowDocs"
        documents.mkdir()
        for name in ("brief.md", "contracts.md", "architecture.md", "collaboration.md", "increments.md", "handoff.md"):
            (documents / name).write_bytes((self.docs / name).read_bytes())
        for name in ("behavior.py", "acceptanceTests.py"):
            (outer / name).write_bytes((self.app / name).read_bytes())
        self.docs, self.app = documents, outer
        self.path = documents / "validationState.json"
        self.state["sourcePath"] = ".."
        self.write()
        self.validate()
        self.cli("check", "--increment", "I-2")

    def test_generated_caches_do_not_invalidate(self):
        self.validate()
        for directory in ("node_modules", "coverage", "__pycache__"):
            folder = self.app / directory
            folder.mkdir()
            (folder / "generated").write_text("output")
        self.cli("check", "--increment", "I-2")

    def test_missing_or_tampered_logs_block(self):
        self.validate()
        result = self.read()["increments"][0]["attempts"][-1]["results"][0]
        log = self.docs / result["log"]
        log.write_text("forged pass")
        self.cli("check", "--increment", "I-2", success=False)
        log.unlink()
        self.cli("check", "--increment", "I-2", success=False)

    def test_hand_entered_status_is_insufficient(self):
        self.state["increments"][0]["status"] = "passed"
        self.write()
        self.cli("check", "--increment", "I-2", success=False)

    def test_criterion_coverage_cannot_be_omitted_or_replaced_with_build(self):
        self.state["acceptanceCriteria"] = ["AC-1"]
        self.write()
        self.cli("check", "--increment", "I-1", success=False)
        self.read()["acceptanceCriteria"] = ["AC-1", "AC-2"]
        self.state["increments"][0]["checks"][0].update(kind="auxiliary", criteria=[])
        self.write()
        self.cli("check", "--increment", "I-1", success=False)

    def test_unknown_or_forward_dependencies_are_rejected(self):
        self.cli("check", "--increment", "I-unknown", success=False)
        self.state["increments"][0]["dependsOn"] = ["I-2"]
        self.write()
        self.cli("check", "--increment", "I-1", success=False)

    def test_all_previous_increments_required_without_direct_dependency(self):
        self.state["increments"][1]["dependsOn"] = []
        self.write()
        self.cli("check", "--increment", "I-2", success=False)

    def test_final_requires_its_own_integrated_pass(self):
        self.validate("I-2")
        self.cli("check", "--final", success=False)
        self.cli("validate", "--final", "--reviewed")
        self.cli("check", "--final")
        self.read()["final"]["checks"][0]["scope"] = "isolated"
        self.write()
        self.cli("check", "--final", success=False)

    def test_mutating_source_during_validation_blocks_pass(self):
        self.state["increments"][0]["checks"][0]["argv"] = [sys.executable, "-c", "from pathlib import Path; Path('createdDuringTests.py').write_text('changed')"]
        self.write()
        self.validate(success=False)
        self.assertEqual(self.read()["increments"][0]["status"], "blocked")

    def test_corrections_require_flags_preserve_history_and_enforce_limit(self):
        source = self.app / "behavior.py"
        source.write_text("def add(a, b): return 0\ndef valid_title(title): return False\n")
        self.validate(success=False)
        for count in (1, 2):
            source.write_text(source.read_text() + "# correction\n")
            self.validate(success=False)
            self.validate("I-1", "--correction", "I-1", success=False)
            self.assertEqual(self.read()["increments"][0]["correctionPassesUsed"], count)
        self.assertEqual(len(self.state["increments"][0]["attempts"]), 3)
        self.cli("check", "--increment", "I-1", success=False)
        self.validate("I-1", "--correction", "I-1", success=False)

    def test_prerequisite_recovery_does_not_consume_correction(self):
        (self.docs / "handoff.md").unlink()
        self.validate(success=False)
        (self.docs / "handoff.md").write_text("# restored setup\n")
        self.validate()
        self.assertEqual(self.read()["increments"][0].get("correctionPassesUsed", 0), 0)

    def test_timeout_is_blocked_and_lock_is_released(self):
        self.state["increments"][0]["checks"][0].update(argv=[sys.executable, "-c", "import time; time.sleep(10)"], timeoutSeconds=1)
        self.write()
        self.validate(success=False)
        self.assertEqual(self.read()["increments"][0]["status"], "blocked")
        self.assertFalse((self.docs / ".validationGate.lock").exists())

    def test_active_or_stale_lock_denies_both_commands(self):
        (self.docs / ".validationGate.lock").write_text("1234\n")
        self.cli("check", "--increment", "I-1", success=False)
        self.validate(success=False)
        self.assertTrue((self.docs / ".validationGate.lock").exists())

    def test_invalid_json_fails_closed(self):
        self.path.write_text("not json")
        self.cli("check", "--increment", "I-1", success=False)

    def test_external_source_symlinks_fail_closed(self):
        (self.docs / "outside.py").write_text("# external dependency\n")
        (self.app / "link.py").symlink_to(self.docs / "outside.py")
        self.cli("check", "--increment", "I-1", success=False)

    def test_final_correction_limit_cannot_be_bypassed_by_pending_status(self):
        self.state["final"].update(status="pending", correctionPassesUsed=2, attempts=[{"verdict": "failed"}])
        self.write()
        self.cli("check", "--increment", "I-1", success=False)
        self.validate(success=False)

    def test_repeated_command_arguments_are_valid(self):
        self.state["increments"][0]["checks"][0]["argv"] = [sys.executable, "-B", "-B", "-m", "unittest", "acceptanceTests.AcceptanceTests.testAC1"]
        self.write()
        self.validate()

    @unittest.skipUnless(os.name == "posix", "POSIX process-group cleanup")
    def test_timeout_terminates_test_child_processes(self):
        marker = self.docs / "orphanMarker"
        child = "import time; from pathlib import Path; time.sleep(2); Path(" + repr(str(marker)) + ").write_text('orphan')"
        parent = "import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', " + repr(child) + "]); time.sleep(10)"
        self.state["increments"][0]["checks"][0].update(argv=[sys.executable, "-c", parent], timeoutSeconds=1)
        self.write()
        self.validate(success=False)
        time.sleep(1.5)
        self.assertFalse(marker.exists(), "Timeout left a test child running")


if __name__ == "__main__":
    unittest.main()
