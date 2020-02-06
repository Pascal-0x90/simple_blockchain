# -*- coding: utf-8 -*-

'''
In this class, we defne the doubly linked list
which will be used to implement the "chain"
of blocks in our blockchain.

We want a doubly linked list to help for when we
start to iterate things backwards. Just makes it 
easier to go from tail to head instead of iterate
head to tail then output that after we know what 
is in the linked list.
'''

# Define the node object
class node:
    def __init__(self, block=None, next_node=None, last_node=None):
        self.block = block
        self.next_node = next_node
        self.last_node = last_node

    def get_block(self):
        return self.block
    
    def get_next(self):
        return self.next_node

    def get_last(self):
        return self.last_node

    def set_next(self, next_node):
        self.next_node = next_node

    def set_last(self, last_node):
        self.last_node = last_node

class doubly_linked_list:
    # not including a delete feature for this list
    # as we do not need it for the blockchain.
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.size = 0
    
    # This allows us to either insert at the end or at a specific index
    def insert(self, block, index=None):
        # At the end
        if index is None:
            print(True)
            temp = node(block)
            if self.head is None and self.tail is None:
                self.head = temp
                self.tail = temp
            else:
                temp.last_node = self.tail
                self.tail.next_node = temp
                self.tail = temp
        else:
            # at a specific index
            temp = self.head
            x = index - 1
            while x > 0:
                temp = temp.next_node
                x -= 1
            new_node = node(block)
            new_node.next_node = temp.next_node
            new_node.last_node = temp
            temp.next_node.last_node = new_node
            temp.next_node = new_node
        # Always increase the counter of # of nodes
        self.size += 1
    
    def get_size(self):
        # Return the size weve been counting
        return self.size
    
    def print_list(self):
        # Print the list from first to last node
        # (head) --> (tail)
        temp = self.head
        while temp != None:
            print(temp.block)
            temp = temp.next_node
    
    def print_reverse(self):
        # This does the same as the last but last to first node
        # (tail) --> (head)
        temp = self.tail
        while temp != None:
            print(temp.block)
            temp = temp.last_node


    