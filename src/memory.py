from collections import deque

class ShortTermMemory:
    def __init__(self, capacity=5):
        self.buffer = deque(maxlen=capacity)
    def add(self, role, text):
        self.buffer.append({"role": role, "text": text})
    def get(self):
        return list(self.buffer)
