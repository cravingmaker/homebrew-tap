import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.update_stockbit import CASK, main, newer_version


def release(current="2.2.0", latest="2.3.0", outdated=True):
    return [{"cask": "stockbit", "version": {
        "current": current, "latest": latest, "outdated": outdated,
    }}]


class UpdateStockbitTests(unittest.TestCase):
    def test_new_release(self):
        self.assertEqual(newer_version(release()), "2.3.0")

    def test_current_and_ahead_do_not_update(self):
        for latest in ("2.2.0", "2.1.0"):
            self.assertIsNone(newer_version(release(latest=latest, outdated=False)))

    def test_versions_are_compared_numerically(self):
        self.assertEqual(newer_version(release(latest="2.10.0")), "2.10.0")

    def test_rejects_downgrade_and_equivalent_versions(self):
        for latest in ("2.1.0", "2.2.0", "2.2.0.0"):
            with self.subTest(latest=latest), self.assertRaises(ValueError):
                newer_version(release(latest=latest))

    def test_rejects_malformed_skipped_or_unexpected_results(self):
        for result in ([], {}, [None], release() * 2,
                       [{"cask": "stockbit", "status": "error"}],
                       [{"cask": "stockbit", "status": "skipped"}],
                       [{"cask": "different-app", "version": {}}]):
            with self.subTest(result=result), self.assertRaises(ValueError):
                newer_version(result)

    def test_rejects_unsafe_or_unknown_versions(self):
        for latest in (None, "latest", "2.3.0-beta", "2.3.0\nupdated=true", "$(whoami)"):
            with self.subTest(latest=latest), self.assertRaises(ValueError):
                newer_version(release(latest=latest))
        with self.assertRaises(ValueError):
            newer_version(release(outdated="true"))

    @patch("scripts.update_stockbit.subprocess.run")
    def test_no_update_does_not_download_or_mutate(self, run):
        run.return_value.stdout = json.dumps(release(latest="2.2.0", outdated=False))
        with patch.dict("os.environ", {}, clear=True):
            main()
        self.assertEqual(run.call_count, 1)

    @patch("scripts.update_stockbit.subprocess.run")
    def test_updates_through_homebrew_without_git_actions(self, run):
        run.return_value.stdout = json.dumps(release())
        with patch.dict("os.environ", {}, clear=True):
            main()
        self.assertEqual(run.call_args.args[0], [
            "brew", "bump-cask-pr", "--write-only", "--no-audit", "--no-style",
            "--version=2.3.0", CASK,
        ])

    @patch("scripts.update_stockbit.subprocess.run")
    def test_upstream_failure_stops_before_mutation(self, run):
        run.side_effect = subprocess.CalledProcessError(1, "brew")
        with self.assertRaises(subprocess.CalledProcessError):
            main()
        self.assertEqual(run.call_count, 1)

    @patch("scripts.update_stockbit.subprocess.run")
    def test_publishes_outputs_only_after_successful_bump(self, run):
        run.return_value.stdout = json.dumps(release())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            with patch.dict("os.environ", {"GITHUB_OUTPUT": str(output)}):
                main()
            self.assertEqual(output.read_text(), "updated=true\nversion=2.3.0\n")

    @patch("scripts.update_stockbit.subprocess.run")
    def test_failed_download_does_not_publish_update_outputs(self, run):
        run.side_effect = [
            subprocess.CompletedProcess([], 0, stdout=json.dumps(release())),
            subprocess.CalledProcessError(1, "brew bump-cask-pr"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            with patch.dict("os.environ", {"GITHUB_OUTPUT": str(output)}):
                with self.assertRaises(subprocess.CalledProcessError):
                    main()
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
