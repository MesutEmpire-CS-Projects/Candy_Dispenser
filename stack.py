class Empty(Exception):
    def __init__(self, message="The container is empty."):
        self.message = message
        super().__init__(self.message)


# Define the Stack class
class Stack:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self.is_empty():
            return self._items.pop()
        else:
            raise Empty()

    def top(self):
        if not self.is_empty():
            return self._items[-1]
        else:
            raise Empty()

    def getitem(self):
        return self._items

