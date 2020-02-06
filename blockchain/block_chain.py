# -*- coding: utf-8 -*-

import uuid
import linkedlist

'''
Methods needed:
    add
    checkout
    checkin
    log
    remove
    init
    verify
'''

# Define our classes for our library
'''
This is the block class. Has variables which pretain to 
the specification we were given for the block. The types
are dependent on what is passed to it (cause this is python)
so thats why i did not define anything yet. 
'''
class block:
    def __init__(self, prev_hash=None, timestamp=None, case_id=None, evidence_id=None, state=None, data_length=None, data=None):
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.case_id = case_id
        self.evidence_id = evidence_id
        self.state = state
        self.data_length = data_length
        self.data = data

'''
This is the blockchain which is a linked list of the blocks
from the block class definition above. 
'''
# TODO: import blockchain from file
class blockchain:
    def __init__(self, blockchain_location=None, dll=linkedlist.doubly_linked_list()):
        self.dll = dll
        self.blockchain_location = blockchain_location
    
    # TODO: Calculate hash of last block for added block
    def add_block(self, block):
        self.dll.insert(block)
    
    def get_size(self):
        return self.dll.get_size()
    
    def print_bc(self):
        self.dll.print_list()
        
    def print_bc_rev(self):
        self.dll.print_reverse()
        

# Define our library methods

'''
This function is to add new evidence item to bc and
associate it with a given case #.

<create block> --> <add in attributes> --> bc.add(new_block)
'''
def add(bc: blockchain):
    pass

'''
Add a new checkout entry to the bc for a given 
evidence item. 

<create block> --> <add in attributes> --> bc.add(new_block)
'''
def checkout(bc: blockchain):
    pass

'''
Add a new checkout entry to the bc for a given 
evidence item. 

<create block> --> <add in attributes> --> bc.add(new_block)
'''
def checkin(bc: blockchain):
    pass

'''
Display the blockchain entries giving the oldest first unles -r
'''
def log(bc: blockchain, r=False):
    if r:
        bc.print_bc_rev()
    else:
        bc.print_bc()

'''
Prevents any further action from being taken on the evidence item
which the user specifies. The item in question must have the state
of CHECKEDIN to be established before this action can continue.
'''
def remove(bc: blockchain):
    pass

'''
This is the sanity check, only startsup and checks to see if the 
program can read from an initial block
'''
def init(bc: blockchain):
    pass

'''
This will parse the blockchain and validate all 
entries. 
'''
def verify(bc: blockchain):
    pass    
    