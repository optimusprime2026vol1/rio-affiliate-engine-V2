import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/rio.yml"
TRANSPORT = ROOT / ".github/workflows/victor-rio-transport.yml"
DEPLOY = ROOT / ".github/workflows/deploy-pages.yml"
CONTROL = ROOT / "data/production_control.json"


class WorkflowGovernanceTests(unittest.TestCase):
    def test_rio_active_state_uses_locked_self_mode_authority(self):
        state = json.loads(CONTROL.read_text(encoding="utf-8"))
        self.assertEqual(state["production_state"], "ACTIVE")
        self.assertEqual(state["operating_mode"], "GOVERNED_SELF_MODE")
        self.assertTrue(str(state["activation_gate"]).startswith("FOUNDER_APPROVED_"))
        self.assertEqual(state["founder_approval_gate"], "CREDENTIAL_ADMINISTRATION_ONLY")
        self.assertIn("ADD_OR_CREATE_CREDENTIAL", state["founder_approval_required_only_for"])
        self.assertIn("NO_RAW_SECRET_DISCLOSURE", state["mandatory_automatic_controls"])

    def test_autonomous_and_publish_jobs_require_canonical_active_gate(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("needs.production-state.outputs.active == 'true'"), 4)
        self.assertNotIn("git add -A", text)
        self.assertIn("permissions: {contents: read}", text)
        self.assertIn("permissions: {contents: write}", text)

    def test_pages_deployment_uses_canonical_active_gate(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("needs.validate.outputs.production_active == 'true'", text)
        self.assertNotIn("vars.RIO_PRODUCTION_STATE == 'ACTIVE'", text)

    def test_victor_transport_only_stages_task_evidence(self):
        text = TRANSPORT.read_text(encoding="utf-8")
        self.assertIn("git add integration/results/victor_tasks/${VICTOR_RIO_TASK_ID}.json", text)
        self.assertNotIn("git add -A", text)


if __name__ == "__main__":
    unittest.main()
