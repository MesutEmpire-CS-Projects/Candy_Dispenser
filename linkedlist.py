from stack import Empty


class LinkedStack:
    """
    This is a stack implementation using a Linked List
    """

    class _Node:
        """
          This is a node implementation used in a Linked List
          """
        __slot__ = ('_element', '_next')

        def __init__(self, data, next):
            self._element = data
            self._next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def push(self, data):
        """
        Add the item at the top of the stack
        :param data:
        :return: Does not return any value
        """
        self._head = self._Node(data, self._head)
        self._size += 1

    def pop(self):
        """
        It the removes the item at the top of the stack
        :return: Returns the item removed
        """
        if self.is_empty():
            raise Empty()
        oldHead = self._head._element
        self._head = self._head._next
        self._size -= 1
        return oldHead

    def __len__(self):
        """
        Return the number of items in the stack.
        :return: Returns an integer
        """
        return self._size

    def top(self):
        """
        Check for the item at the top of the stack
        :return: If the stack is not empty returns the item at the top of the stack otherwise returns an Empty Exception
        """
        if self.is_empty():
            raise Empty()
        return self._head._element

    def is_empty(self):
        """
        Check whether the stack is empty
         :return: Returns a boolean
         """
        return self._size == 0

    # def get_items(self):
    #     """
    #     Retrieve the items in the stack
    #     :return: Returns all the items in the stack
    #     """
    #     current = self._head
    #     while current:
    #         yield current._element
    #         current = current._next


if __name__ == '__main__':
    stack = LinkedStack()
    stack.push(12)
    stack.push(2)
    stack.push(24)
    stack.push(45)
    stack.push(54)
