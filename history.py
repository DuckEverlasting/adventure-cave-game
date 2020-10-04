class History:
    def __init__(self, limit=20):
        self.stack = []
        self.limit = limit
        self.steps_back = 0

    def push(self, value):
        if len(value) is 0:
            return
        self.steps_back = 0
        self.stack.append(value)
        if len(self.stack) > self.limit:
            self.stack.pop(0)

    def get_prev(self):
        if len(self.stack) > self.steps_back:
            self.steps_back += 1
            return self.stack[-self.steps_back]
        else:
            return None

    def get_next(self):
        if self.steps_back > 1:
            self.steps_back -= 1
            return self.stack[-self.steps_back]
        elif self.steps_back == 1:
            self.steps_back -= 1
        return ""
