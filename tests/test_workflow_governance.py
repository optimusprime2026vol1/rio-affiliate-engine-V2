import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/rio.yml"
TRANSPORT = ROOT / ".github/workflows/victor-rio-transport.yml"
CONTROL = ROOT / "data/production_control.json"

class WorkflowGovernanceTests(unittest.TestCase):
    def test_rio_is_canonically_parked(self):
        state = json.loads(CONTROL.read_text(encoding="utf-8"))
        self.assertEqual(state["production_state"], "PARKED")
        self.assertEqual(state["activation_gate"], "EXPLICIT_FOUNDER_APPROVAL_REQUIRED")

    def test_autonomous_and_publish_jobs_require_active_gate(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("vars.RIO_PRODUCTION_STATE == 'ACTIVE'"), 4)
        self.assertNotIn("git add -A", text)
        self.assertIn("permissions: {contents: read}", text)
        self.assertIn("permissions: {contents: write}", text)

    def test_victor_transport_only_stages_task_evidence(self):
        text = TRANSPORT.read_text(encoding="utf-8")
        self.assertIn("git add integration/results/victor_tasks/${VICTOR_RIO_TASK_ID}.json", text)
        self.assertNotIn("git add -A", text)

if __name__ == "__main__":
    unittest.main()
