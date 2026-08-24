#!/usr/bin/env python3
"""RIO SOUL runtime integrity check.

Hard fail-closed governance is now enabled for consequential execution. This
script refreshes the canonical SOUL runtime status after heartbeat health and
validator state have been refreshed. Diagnostics remain available on failure.
"""
import json
from soul_gate import evaluate


def inspect_runtime():
    result = evaluate(
        action="heartbeat_runtime_binding",
        require_health=True,
        require_kill_clear=True,
        write_status=True,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(inspect_runtime())
