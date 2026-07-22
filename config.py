"""
config.py
---------
Central place to define what this agent is, and what it is allowed to
answer. Edit the values below to change the agent's name/scope — every
other file (prompts.py, engine/guard.py) reads from here, so you only
need to touch this one file to re-purpose the bot.
"""

# Shown to the user and used inside prompts so the model knows its own identity.
BOT_NAME = "AI Task Planner Agent"

# One or two sentences describing EXACTLY what this agent is for.
# The scope guard uses this to decide what counts as "on topic".
BOT_SCOPE_DESCRIPTION = (
    "Taking a user's GOAL (something they want to accomplish, e.g. "
    "'plan a birthday party', 'learn Python in a month', 'organize a house "
    "move'), breaking it into an ordered list of small actionable tasks, "
    "and then executing/explaining each task step by step."
)

# Message shown when a user message is judged OFF_TOPIC by the scope guard.
OFF_TOPIC_MESSAGE = (
    f"I'm {BOT_NAME} — I only help with breaking a GOAL down into steps and "
    "working through them (things like 'plan a trip', 'prepare for an "
    "interview', 'launch a small website'). That question is outside what "
    "I'm built for, so I can't help with it here. Please ask me something "
    "in the form of a goal or task you'd like planned and executed."
)
