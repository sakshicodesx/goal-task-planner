"""
main.py
-------
Entry point for the AI Task Planner Agent.

Run with:
    python main.py
"""

from engine.coordinator import Coordinator


def main():
    print("=== AI Goal Task Planner Agent ===")
    print("Type a goal and the agent will plan and execute the steps.")
    print("Type 'exit' to quit.\n")

    coordinator = Coordinator()

    while True:
        goal = input("Enter your goal: ").strip()
        if goal.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not goal:
            continue

        coordinator.run(goal)
        print("-" * 50)


if __name__ == "__main__":
    main()
