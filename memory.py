"""
memory.py
---------
A lightweight, dependency-free chat buffer.

Instead of relying on LangChain's older memory classes (many of which are
being deprecated), this keeps a simple list of messages in RAM and persists
them to a JSON file on disk. Simple, transparent, and future-proof.
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class ChatBuffer:
    def __init__(self, save_path: str = "chat_history.json"):
        self.save_path = save_path
        self.history: List[Dict] = []
        self._load()

    def _load(self):
        """Load existing history from disk, if any."""
        if os.path.exists(self.save_path):
            with open(self.save_path, "r", encoding="utf-8") as f:
                try:
                    self.history = json.load(f)
                except json.JSONDecodeError:
                    self.history = []

    def save(self):
        """Persist the current history to disk."""
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def add(self, role: str, content: str):
        """Add a message to the buffer and immediately save it."""
        self.history.append(
            {
                "role": role,  # "user" | "planner" | "executor" | "system"
                "content": content,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
        )
        self.save()

    def get_history(self) -> List[Dict]:
        return self.history

    def as_text(self, last_n: int = 10) -> str:
        """
        Returns the last N messages formatted as plain text,
        useful for injecting recent context into a prompt.
        """
        recent = self.history[-last_n:]
        lines = [f"{m['role']}: {m['content']}" for m in recent]
        return "\n".join(lines)

    def clear(self):
        self.history = []
        self.save()
