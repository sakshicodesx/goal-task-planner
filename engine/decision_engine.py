"""
engine/decision_engine.py
--------------------------
Simple rule-based decision engine.

After each task is executed, this decides whether to:
  - "continue"  -> move on to the next task
  - "retry"     -> re-run the current task (e.g. execution looked like an error)
  - "stop"      -> halt the whole plan (e.g. task result signals a hard failure)

Kept rule-based (no extra LLM call) so it's fast, cheap, and predictable.
You can swap the logic here for an LLM-based judge later without touching
anything else in the project.
"""

FAILURE_KEYWORDS = ["error", "failed", "cannot", "unable to", "not possible"]


class DecisionEngine:
    def __init__(self, max_retries: int = 2):
        self.max_retries = max_retries
        self._retry_counts = {}

    def decide(self, task: str, result: str) -> str:
        result_lower = result.lower()

        looks_like_failure = any(kw in result_lower for kw in FAILURE_KEYWORDS)

        if not looks_like_failure:
            return "continue"

        retries_so_far = self._retry_counts.get(task, 0)
        if retries_so_far < self.max_retries:
            self._retry_counts[task] = retries_so_far + 1
            return "retry"

        return "stop"
