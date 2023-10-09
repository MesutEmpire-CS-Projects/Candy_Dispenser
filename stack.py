class Empty(Exception):
    def __init__(self, message="The container is empty."):
        self.message = message
        super().__init__(self.message)


# Define the Stack class
class Stack:
    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise Empty()

    def top(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise Empty()

