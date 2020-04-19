# -*- coding: utf-8 -*-

import uuid
import os
import sys
import time
from datetime import timezone, datetime
import struct
import linkedlist
import hashlib
DEBUG = False

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
    def set_prev_hash(self, block, prev_hash=None):
        if block == None and prev_hash != None:
            self.prev_hash = prev_hash
            return
        if block == None:
            self.prev_hash = None
        else:
            self.prev_hash = block.get_self_hash() 
        
    def set_timestamp(self):
        # This will set timestamp based on current time
        self.timestamp = time.time()

    def set_old_timestamp(self, data):
        self.timestamp = data
        
    def set_case_id(self, case_id): # Case id is bytes at this point
        if case_id == None:
            self.case_id = None
            return 0
        uid = uuid.UUID(case_id.hex())
        self.case_id = uid.bytes
        return 0
    
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

    def get_self_hash(self):
        if self.state == "INITIAL":
            guts = "\x00".encode() + bytes(struct.pack("d",self.timestamp)) + "\x00".encode() + "\x00".encode() + self.state.encode() + bytes(self.data_length) + self.data.encode()
        else:
            guts = self.prev_hash.encode() + bytes(struct.pack("d",self.timestamp)) + uuid.UUID(self.case_id.hex()).bytes + bytes(self.evidence_id) + self.state.encode() + bytes(self.data_length) + self.data.encode()
        self_hash = hashlib.sha1(guts)
        return self_hash.hexdigest()
    
'''
This is the blockchain which is a linked list of the blocks
from the block class definition above. 
'''
# Global Struct object
s = struct.Struct("20s d 16s I 11s I")

# TODO: import blockchain from file
class blockchain:
    # blockchain()
    def __init__(self, dll=linkedlist.doubly_linked_list()):
        self.dll = dll
        self.file_path = os.environ.get("BCHOC_FILE_PATH") 
    
    # TODO: Calculate hash of last block for added block
    def add_block(self, block):
        self.dll.insert(block)
        
    def get_recent(self):
        return self.dll.tail.block
    
    def get_list(self):
        return self.dll.list()
    
    def get_size(self):
        return self.dll.get_size()
    
    def new_evidence_add(self, case_id, item_id): # Item_id should be a list of items, even if just 1
        if len(item_id) < 1:
            return 0
        print("Case:", str(uuid.UUID(bytes().fromhex(case_id).hex())))
        for item in item_id:
            new_block = block()
            new_block.set_prev_hash(self.get_recent())
            new_block.set_timestamp()
            new_block.set_case_id(bytes().fromhex(case_id))
            new_block.set_evidence_id(item)
            new_block.set_state("CHECKEDIN")
            new_block.set_data_length(0)
            new_block.set_data("")
            self.add_block(new_block)
            print("Added item:", item)
            print("\tStatus:", new_block.get_state())
            print("\tTime of Action:", str(datetime.fromtimestamp(new_block.get_timestamp(),tz=timezone.utc).isoformat()).replace("+00:00","Z"))
        self.export_bc()

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
        return None
    
    def export_bc(self):
        blocks = self.get_list()
        fp = open(self.file_path, "wb")
        #blocks is an array of nodes/blocks from the linked list
        for i in blocks:
            #get the data from the block
            temp_hash = i.get_prev_hash()
            temp_time = i.get_timestamp()
            temp_case_id = i.get_case_id()
            temp_evidence_id = i.get_evidence_id()
            temp_state = i.get_state()
            temp_data_length = i.get_data_length()
            temp_data = i.get_data()
            if DEBUG:
                print(str(temp_hash)+' '+str(temp_time)+' '+str(temp_case_id)+' '+str(temp_evidence_id)+' '+str(temp_state)+' '+str(temp_data_length))
            #turn strings to bytes
            
            if temp_state == "INITIAL":
                temp_hash = bytes(str(temp_hash), 'utf-8')
                temp_case_id = bytes(str(temp_case_id),'utf-8')
                temp_evidence_id = 0
                temp_state = bytes(str(temp_state), 'utf-8')
                temp_data = bytes(str(temp_data), 'utf-8')
            else:
                temp_hash = bytes(str(temp_hash), 'utf-8')
                temp_case_id = uuid.UUID(temp_case_id.hex()).bytes
                temp_state = bytes(str(temp_state), 'utf-8')
                temp_data = bytes(str(temp_data), 'utf-8')

            header = struct.pack("20s d 16s I 11s I", temp_hash,temp_time,temp_case_id, temp_evidence_id,temp_state,temp_data_length)
            formatstring = str(temp_data_length)+"s"
            footer = struct.pack(formatstring, temp_data)
            
            fp.write(header)
            fp.write(footer)

        fp.close()
        
    def import_bc(self):
        # If cant find file, throw err
        f = open(self.file_path, "rb")
        #get the sizes for the format
        
        section_size= struct.calcsize("20s d 16s I 11s I")
        data_size = None

        temp_hash = None
        temp_time = None
        temp_case_id =None
        temp_evidence_id =None
        temp_state = None
        temp_data_length = None
        temp_data = None

        f.seek(0,0)
        file_location =0
        
        while True:
            #check if there is another byte
            useless = f.read(1)
            if DEBUG:
                    print(useless)
                    print(str(type(useless)))
            if useless == b'':
                break
            else:
                #return back to previous location
                f.seek(file_location, 0)
            
            #unpack data
            temp_hash, temp_time, temp_case_id, temp_evidence_id, temp_state, temp_data_length = struct.unpack("20s d 16s I 11s I", f.read(section_size))
                        
            formatstring = str(temp_data_length)+"s"
            data_size = struct.calcsize(formatstring)
            temp_data = struct.unpack(formatstring, f.read(data_size))[0]
            #increment file_location 
            file_location = file_location+ section_size + data_size
            
            if DEBUG:
                print(str(temp_hash)+' '+str(temp_time)+' '+str(temp_case_id)+' '+str(temp_evidence_id)+' '+str(temp_state)+' '+str(temp_data_length)+' '+str(temp_data))
                print(str(type(temp_hash))+' '+str(type(temp_time))+' '+str(type(temp_case_id))+' '+str(type(temp_evidence_id))+' '+str(type(temp_state))+' '+str(type(temp_data_length))+' '+str(type(temp_data)))

            #format the variables back to how we like them
            temp_hash = temp_hash.decode("utf-8")
            temp_time = int(temp_time)
            temp_case_id = temp_case_id # To convert to readable do uuid.UUID(case_id.hex())
            temp_state = temp_state.decode("utf-8")[:-4]
            temp_data = temp_data.decode("utf-8")[:-1]

            if DEBUG:
                print(str(temp_hash)+' '+str(temp_time)+' '+str(temp_case_id)+' '+str(temp_evidence_id)+' '+str(temp_state)+' '+str(temp_data_length)+' '+str(temp_data))
                print(str(type(temp_hash))+' '+str(type(temp_time))+' '+str(type(temp_case_id))+' '+str(type(temp_evidence_id))+' '+str(type(temp_state))+' '+str(type(temp_data_length))+' '+str(type(temp_data)))
            
            #if we find that this is an initial block, then set the values to be None types.
            #we can keep this as the only check/verificaiton that "this" is the initial block , or specifically check each variable to be == "None"
            if 'INITIAL' in temp_state:
                if DEBUG:
                    print("Found the initial block")
                temp_hash = None
                temp_case_id = None

            #some variation on this to add 
            new_block = block()
            new_block.set_old_timestamp(temp_time)
            new_block.set_prev_hash(None, temp_hash)
            new_block.set_case_id(temp_case_id)
            new_block.set_evidence_id(temp_evidence_id)
            new_block.set_state(temp_state)
            new_block.set_data_length(temp_data_length)
            new_block.set_data(temp_data)
            self.add_block(new_block)
            #some break when reaching the end of the file
    
        f.close()
        
    # Checks for initial block
    def init(self, check_only=False):
        #check if there is a INITIAL block
        #TODO: do stuff to check
        '''
        if INITIAL_found:
            print('Blockchain file found with INITIAL block.')
        else:
            #TODO:  should this go here too?
            #       or maybe raise an exception so it goes into the
            #       next seciton? -----> but then it would erase the data
            #       previously stored. But if its not found then the BC was
            #       altered and no longer authentic?---> probably 
            #       wont be checked.
            print('Blockchain file not found. Created INITIAL block.')
        '''
        if os.path.exists(self.file_path):
            self.import_bc()
            #find the init block
            wasFound = self.search_by_id(0)
            # Check if it has some initial identifier
            if wasFound is not None:
                state = wasFound.get_state()
                if wasFound.get_state() == "INITIAL":
                    if check_only is False:
                        print('Blockchain file found with INITIAL block.')
                else:
                    if DEBUG:
                        print("Blockchain Found. No Initial Block.")
                    sys.exit(1)
                    # Maybe do something here for adding in INITBLOCK or just die
        else: 
            if check_only is False:
                print("Blockchain file not found. Creating Initial Block.")
            # File didnt exit or no iniitiial block, we must make our own
            new_block = block()
            new_block.set_timestamp()
            new_block.set_prev_hash(None)
            new_block.set_case_id(None)
            new_block.set_evidence_id(None)
            new_block.set_state("INITIAL")
            new_block.set_data_length(14)
            new_block.set_data("Initial Block")
            self.add_block(new_block)
        if check_only is False:
            self.export_bc()
        
        


        
        


#     '''
#     Utilities for verify
#     '''
#     def verify_parents(blocklist):
#         for i in blocklist:
#             temp_hash = i.get_prev_hash()
#             if temp_hash == None:
#                 return i.get_case_id()
#         return None

#     def verify_dupe(blocklist):
#         seen = {}
#         dupes = []
#         for i in blocklist:
#             temp_hash = i.get_prev_hash()
#             temp_block = hashlib.md5(i).hexdigest()
#             for temp_hash not in seen:
#                 seen[temp_hash] = 1
#             else:
#                 if seen[temp_hash] == 1:
#                     dupes.append(temp_block)
#                     dupes.append(temp_hash)
#                 seen[temp_hash] += 1
#         if len(dupes) != 0:
#             return dupes[0]
#         return None

#     def verify_checksum(blocklist):
#         pass # Pass for now

#     def verify_checkin(blocklist):
#         pass # Pass for now

    
#     '''
#     This will parse the blockchain and validate all 
#     entries. 
#     '''
#     def verify(self):
#         transactions = self.get_size()
#         blocklist = self.get_list()
#         print("Transactions in blockchain: {}".format(transactions, get_type(transactions))

#         parents = verify_parents(blocklist)
#         dupe = verify_dupe(blocklist)
#         checksum = verify_checksum(blocklist)
#         checkin = verify_checkin(blocklist)

#         if (parents != None):
#             state = 'ERROR'
#             print("State of blockchain: {}").format(state,get_type(state))
#             print("Bad block: {}").format(parents,get_type(parents))
#             print("Parent block: NOT FOUND")
#         elif (dupe != None):
#             state = 'ERROR'
#             print("State of blockchain: {}").format(state,get_type(state))
#             print("Bad block: {}").format(dupe[0],get_type(dupe[0]))
#             print("Parent block: {}").format(dupe[1],get_type(dupe[1]))
#             print("Two blocks found with same parent.")
#         elif (checksum != None):
#             state = 'ERROR'
#             print("State of blockchain: {}").format(state,get_type(state))
#             print("Bad block: {}").format(checksum,get_type(checksum))
#             print("Block contents do not match block checksum.")
#         elif (checkin != None):
#             state = 'ERROR'
#             print("State of blockchain: {}").format(state,get_type(state))
#             print("Bad block: {}").format(checkin,get_type(checkin))
#             print("Item checked out or checked in after removal from chain.")
#         else:
#             state = 'CLEAN'
#             print("State of blockchain: {}").format(state,get_type(state))

            
            
        
         
            
# # Define our library methods

# '''
# This function is to add new evidence item to bc and
# associate it with a given case #.

# <create block> --> <add in attributes> --> bc.add(new_block)
# '''
# def add(bc: blockchain, case_id, item_id): # where item_id is a list
#     for item in item_id:
        
        

# '''
# Add a new checkout entry to the bc for a given 
# evidence item. 

# <create block> --> <add in attributes> --> bc.add(new_block)
# '''
# def checkout(bc: blockchain, item_id):
#     # Despite this one taking the item_id, the spec only says one ID
#     # will be/should be passed. So we take the first element
#     iden = int(item_id[0])
#     ref_block = bc.search_by_id(iden)
#     if ref_block.get_case_id is not None:
#         new_block = block()
#         new_block.set_prev_hash(bc.get_recent())
#         new_block.set_timestamp()
#         new_block.set_case_id(str(ref_block.get_case_id())) # Send string version
#         new_block.set_evidence_id(iden)
#         new_block.set_state("CHECKEDOUT")
#         new_block.set_data_length(0)
#         new_block.set_data(None)
#         bc.add_block(new_block)
        

# '''
# Add a new checkout entry to the bc for a given 
# evidence item. 

# <create block> --> <add in attributes> --> bc.add(new_block)
# '''
# def checkin(bc: blockchain, item_id):
#     iden = int(item_id[0])
#     ref_block = bc.search_by_id(iden)
#     if ref_block.get_case_id is not None:
#         new_block = block()
#         new_block.set_prev_hash(bc.get_recent())
#         new_block.set_timestamp()
#         new_block.set_case_id(str(ref_block.get_case_id())) # Send string version
#         new_block.set_evidence_id(iden)
#         new_block.set_state("CHECKEDIN")
#         new_block.set_data_length(0)
#         new_block.set_data(None)
#         bc.add_block(new_block)

# '''
# Display the blockchain entries giving the oldest first unles -r
# '''
# def log(bc: blockchain, r=False):
#     if r:
#         bc.print_bc_rev()
#     else:
#         bc.print_bc()

# '''
# Prevents any further action from being taken on the evidence item
# which the user specifies. The item in question must have the state
# of CHECKEDIN to be established before this action can continue.
# '''
# def remove(bc: blockchain):
#     pass

# '''
# This is the sanity check, only startsup and checks to see if the 
# program can read from an initial block
# '''
# def init(bc: blockchain):
#     pass


    
