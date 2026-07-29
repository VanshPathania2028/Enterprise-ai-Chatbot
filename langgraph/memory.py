class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, role: str, message: str):
        self.history.append(f"{role}: {message}")

    def get(self):
        return "\n".join(self.history)

    def clear(self):
        self.history = []

memory = ConversationMemory()