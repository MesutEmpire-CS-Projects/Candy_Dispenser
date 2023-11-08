class Empty(Exception):
    def __init__(self, message="The container is empty."):
        self.message = message
        super().__init__(self.message)


# Define the Stack class
class ArrayStack:
    """
    This is a stack implementation using a List
    """

    def __init__(self):
        self.items = []

    def __len__(self):
        """
        Return the number of items in the stack.
        :return: Returns an integer
        """
        return len(self.items)

    def is_empty(self):
        """
        Check whether the stack is empty
         :return: Returns a boolean
         """
        return len(self.items) == 0

    def push(self, item):
        """
        Add the item at the top of the stack
        :param item:
        :return: Does not return any value
        """
        self.items.append(item)

    def pop(self):
        """
        It the removes the item at the top of the stack
        :return: Returns the item removed
        """
        if not self.is_empty():
            return self.items.pop()
        else:
            raise Empty()

    def top(self):
        """
        Check for the item at the top of the stack
        :return: If the stack is not empty returns the item at the top of the stack otherwise returns an Empty Exception
        """
        if not self.is_empty():
            return self.items[-1]
        else:
            raise Empty()


if __name__ == '__main__':
    stack = ArrayStack()
    stack.push(12)
    stack.push(2)
    stack.push(24)
    stack.push(45)
    stack.push(54)
