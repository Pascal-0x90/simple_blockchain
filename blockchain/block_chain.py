# -*- coding: utf-8 -*-

import uuid
import os
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
        self.prev_hash = prev_hash          # Hash type?
        self.timestamp = timestamp          # timestamp type?
        self.case_id = case_id              # UUID
        self.evidence_id = evidence_id      # int
        self.state = state                  # String 
        self.data_length = data_length      # Int
        self.data = data                    # String
    
    # Define setters
    def set_prev_hash(self, hash_val):
        self.prev_hash = hash_val 
        
    def set_timestamp(self):
        # This will set timestamp based on current time
        # TODO: Self set timestamp
        pass
        
    def set_case_id(self, case_id): # Case id is still a string at this point
        uid = uuid.UUID(case_id)
        self.case_id = uid
    
    def set_evidence_id(self, evidence_id):
        self.evidence_id = evidence_id
        
    def set_state(self, state):
        self.state = state
        
    def set_data_length(self, data_length):
        self.data_length = data_length
        
    def set_data(self, data):
        self.data = data
        
    # Define getters
    def get_prev_hash(self):
        return self.prev_hash   # Return hash
    
    def get_timestamp(self):
        return self.timestamp   # return timestamp
    
    def get_case_id(self):
        return self.case_id     # returns UUID
        
    def get_evidence_id(self):
        return self.evidence_id # return int
    
    def get_state(self):
        return self.state       # return string
    
    def get_data_length(self):
        return self.data_length # Return data length int
    
    def get_data(self):
        return self.data        # Return data string
    
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
        
    def get_recent(self):
        return self.dll.tail
    
    def get_size(self):
        return self.dll.get_size()
    
    # TODO: Change this to format properly    
    def print_bc(self):
        self.dll.print_list()
    
    # TODO: Change this to format properly        
    def print_bc_rev(self):
        self.dll.print_reverse()
        
    def search_by_id(self, item_id):
        temp = self.dll.head
        while temp != None:
            if temp.block.get_evidence_id() == item_id:
                return temp.block
            else:
                temp = temp.next_node
        return block()

# Define our library methods

'''
This function is to add new evidence item to bc and
associate it with a given case #.

<create block> --> <add in attributes> --> bc.add(new_block)
'''
def add(bc: blockchain, case_id, item_id): # where item_id is a list
    for item in item_id:
        new_block = block()
        new_block.set_prev_hash(bc.get_recent())
        new_block.set_timestamp()
        new_block.set_case_id(case_id)
        new_block.set_evidence_id(item)
        new_block.set_state("CHECKEDIN")
        new_block.set_data_length(0)
        new_block.set_data(None)
        bc.add_block(new_block)
        

'''
Add a new checkout entry to the bc for a given 
evidence item. 

<create block> --> <add in attributes> --> bc.add(new_block)
'''
def checkout(bc: blockchain, item_id):
    # Despite this one taking the item_id, the spec only says one ID
    # will be/should be passed. So we take the first element
    iden = int(item_id[0])
    ref_block = bc.search_by_id(iden)
    if ref_block.get_case_id is not None:
        new_block = block()
        new_block.set_prev_hash(bc.get_recent())
        new_block.set_timestamp()
        new_block.set_case_id(str(ref_block.get_case_id())) # Send string version
        new_block.set_evidence_id(iden)
        new_block.set_state("CHECKEDOUT")
        new_block.set_data_length(0)
        new_block.set_data(None)
        bc.add_block(new_block)
        

'''
Add a new checkout entry to the bc for a given 
evidence item. 

<create block> --> <add in attributes> --> bc.add(new_block)
'''
def checkin(bc: blockchain, item_id):
    iden = int(item_id[0])
    ref_block = bc.search_by_id(iden)
    if ref_block.get_case_id is not None:
        new_block = block()
        new_block.set_prev_hash(bc.get_recent())
        new_block.set_timestamp()
        new_block.set_case_id(str(ref_block.get_case_id())) # Send string version
        new_block.set_evidence_id(iden)
        new_block.set_state("CHECKEDIN")
        new_block.set_data_length(0)
        new_block.set_data(None)
        bc.add_block(new_block)

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
    