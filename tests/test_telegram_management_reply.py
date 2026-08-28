import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "telegram_management_reply.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("telegram_management_reply", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TelegramManagementReplyTests(unittest.TestCase):
    def test_build_reply_uses_verified_result_fields(self):
        text = MODULE.build_reply(
            {
                "task_id": "victor-rio-test-1",
                "execution_status": "COMPLETED",
                "strict_supervision": {
                    "status": "ACTIVE_GOVERNED",
                    "objective_alignment": "ALIGNED",
                    "solution": "Continue governed execution",
                    "next_action": "Run next cycle",
                    "evidence": ["result.json"],
                },
            }
        )
        self.assertIn("RIO management-group revert", text)
        self.assertIn("Status: ACTIVE_GOVERNED", text)
        self.assertIn("Task ID: victor-rio-test-1", text)


if __name__ == "__main__":
    unittest.main()
