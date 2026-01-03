class Memory:
    # todo à completer
    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key)

    def forget(self, key):
        if key in self.memory:
            del self.memory[key]