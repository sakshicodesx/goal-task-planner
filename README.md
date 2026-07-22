# AI Task Planner Agent

A small multi-agent system that takes a **goal** you type in, breaks it down
into an ordered list of small tasks, and then executes/explains each task
one by one — with retry/stop logic and persistent chat history.

Built with [LangChain](https://python.langchain.com/) + [Groq](https://console.groq.com)
(free tier, no credit card needed).

## How it works

```
your goal
   │
   ▼
ScopeGuard  ──► off-topic? ──► polite refusal, stop here
   │ on-topic
   ▼
PlannerAgent   → turns the goal into a numbered list of tasks
   │
   ▼
ExecutorAgent  → runs/explains each task, one at a time
   │
   ▼
DecisionEngine → continue / retry / stop, based on the result
   │
   ▼
ChatBuffer     → logs everything to chat_history.json
```

| File | Responsibility |
|---|---|
| `main.py` | CLI entry point / input loop |
| `config.py` | Bot identity + allowed scope + off-topic message (edit this to re-purpose the bot) |
| `prompts.py` | All prompt templates (guard, planner, executor) |
| `engine/guard.py` | Rejects messages outside the bot's defined use case |
| `agents/planner.py` | Breaks a goal into tasks |
| `agents/executor.py` | Executes a single task |
| `engine/decision_engine.py` | Rule-based continue/retry/stop logic |
| `engine/coordinator.py` | Wires all of the above together |
| `memory.py` | Lightweight JSON-backed chat history |
| `models.py` | LLM configuration (Groq / LangChain) |

## Staying on-topic

This agent is restricted to one job: **turning goals into plans and executing
them**. Before anything else runs, `engine/guard.py` asks the model to
classify your message as `ON_TOPIC` or `OFF_TOPIC` against the description in
`config.py`.

- **On-topic** ("plan a birthday party", "help me learn Python in a month") →
  proceeds to planning as normal.
- **Off-topic** (general trivia, small talk, unrelated coding help, requests
  to ignore instructions, questions about the system prompt, etc.) → the
  agent replies with a short, polite message explaining what it *is* for
  instead of answering, and stops there — no planning/execution call is
  made.

To change what counts as "on-topic," or to re-brand the bot for a different
use case, edit **`config.py`** only:

```python
BOT_NAME = "AI Task Planner Agent"
BOT_SCOPE_DESCRIPTION = "..."   # what the bot is allowed to help with
OFF_TOPIC_MESSAGE = "..."      # what it says when it declines
```

Everything else (`prompts.py`, `engine/guard.py`) reads from these values, so
you never have to touch the guard logic itself.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a free API key at [console.groq.com/keys](https://console.groq.com/keys)
   (no credit card required) and paste it into `.env`:
   ```
   GROQ_API_KEY=your_real_key_here
   ```
3. Run it:
   ```bash
   python main.py
   ```
4. Type a goal at the prompt, e.g.:
   ```
   Enter your goal: plan a weekend hiking trip
   ```
   Type `exit` to quit.

## Configuration

All of this is set in `.env`:

| Variable | Purpose | Default |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key | *(required)* |
| `MODEL_NAME` | Which Groq-hosted model to use | `llama-3.3-70b-versatile` |
| `MODEL_TEMPERATURE` | 0 = focused/deterministic, 1 = more creative | `0.3` |

## Notes

- Chat history persists to `chat_history.json` in the working directory
  between runs. Delete that file (or call `ChatBuffer.clear()`) to reset it.
- The `DecisionEngine` is intentionally simple/rule-based (keyword matching
  for failure signals) so it's fast, free, and predictable — swap it for an
  LLM-based judge later if you need smarter retry logic.

## License

Released under the [MIT License](LICENSE) — see the `LICENSE` file for the
full text.
