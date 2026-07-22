from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER = REPOSITORY_ROOT / "scripts" / "build_evals.py"


class EvalBuilderTests(unittest.TestCase):
    def test_committed_combined_inventory_is_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS [EVALS_COMBINED_CURRENT]", result.stdout)

    def test_unsupported_boundary_does_not_require_out_of_scope_claim_analysis(self) -> None:
        inventory = json.loads(
            (REPOSITORY_ROOT / "skills/strategic-advisor/evals/evals.json").read_text(
                encoding="utf-8"
            )
        )
        boundary = next(
            item for item in inventory["evals"] if item["id"] == "CROSS-BOUNDARY-PER-001"
        )
        self.assertFalse(
            any("One spouse" in assertion for assertion in boundary["assertions"])
        )
        self.assertTrue(
            any("zero professional lenses" in assertion for assertion in boundary["assertions"])
        )


if __name__ == "__main__":
    unittest.main()
