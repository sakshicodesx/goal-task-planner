"""
engine/coordinator.py
----------------------
The Coordinator ties everything together:
  Planner  -> generates tasks from a goal
  Executor -> runs each task
  DecisionEngine -> decides continue / retry / stop after each task
  ChatBuffer -> logs everything so history persists across runs
"""

from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from engine.decision_engine import DecisionEngine
from engine.guard import ScopeGuard
from memory import ChatBuffer


class Coordinator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.decision_engine = DecisionEngine()
        self.guard = ScopeGuard()
        self.memory = ChatBuffer()

    def run(self, goal: str):
        self.memory.add("user", f"GOAL: {goal}")

        # --- Scope check -----------------------------------------------
        # Reject anything outside this agent's defined use case BEFORE
        # spending a planning/execution call on it.
        if not self.guard.is_on_topic(goal):
            refusal = self.guard.refusal_message()
            self.memory.add("system", f"Rejected off-topic input: {refusal}")
            print(refusal)
            return [{"task": goal, "result": refusal, "decision": "off_topic"}]

        history_text = self.memory.as_text()
        tasks = self.planner.plan(goal, history=history_text)
        self.memory.add("planner", "Planned tasks:\n" + "\n".join(tasks))

        print(f"\nPlan for goal: '{goal}'")
        for i, t in enumerate(tasks, 1):
            print(f"  {i}. {t}")
        print()

        results = []
        i = 0
        while i < len(tasks):
            task = tasks[i]
            print(f"--> Executing task {i + 1}/{len(tasks)}: {task}")

            history_text = self.memory.as_text()
            result = self.executor.execute(task, history=history_text)
            self.memory.add("executor", f"Task: {task}\nResult: {result}")

            decision = self.decision_engine.decide(task, result)
            results.append({"task": task, "result": result, "decision": decision})

            print(f"    Result: {result}")
            print(f"    Decision: {decision}\n")

            if decision == "continue":
                i += 1
            elif decision == "retry":
                # stay on the same task index, try again
                continue
            elif decision == "stop":
                print("Stopping plan execution due to unresolved failure.")
                break

        self.memory.add("system", "Plan execution finished.")
        return results
