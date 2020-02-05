# -*- coding: utf-8 -*-

import argparse
import uuid # For the case id. Probably used in the caseID module
import sys

'''
Arguments:
    add
    checkout
    checkin
    log
    remove
    init
    verify
    case id:        -c <id>
    reverse         -r --reverse
    item_id         -i <id>
    num_entries:    -n <num of entries>
    reason          -y <reason> , --why <reason>
    owner           -o <ownder>
'''

# Our main function
def main():
    # Initialize our parser
    parser = argparse.ArgumentParser(description='Block-Chain of Custody Python Implementation')
    
    # Define our positional arguments (Defined as: <command>, use args, default state, type of arg, help statement)
    parser.add_argument('add', nargs='?', default=False, type=bool, help='Add a new evidence item to the blockchain and associate it with the given case identifier')
    parser.add_argument('checkout', nargs='?', default=False, type=bool, help='Add a new checkout entry to the chain of custody for the given evidence item')
    parser.add_argument('checkin', nargs='?', default=False, type=bool, help='Add a new checkin entry to the chain of custody for the given evidence item')
    parser.add_argument('log', nargs='?', default=False, type=bool, help='Display the blockchain entries giving the oldest first (unless -r is given)')
    parser.add_argument('remove', nargs='?', default=False, type=bool, help='Prevents any further action from being taken on the evidence item specified')
    parser.add_argument('init', nargs='?', default=False, type=bool, help='Sanity check. Only starts up and checks for the initial block')
    parser.add_argument('verify', nargs='?', default=False, type=bool, help='Parse the blockchain and validate all entries')
    
    # Define our optional arguments
    parser.add_argument('-c', type=str, help='Specifies the case identifier that the evidence is associated with', required=False)
    parser.add_argument('-i', type=int, help='Specifies the evidence item’s identifier', required=False)
    parser.add_argument('-n', type=int, help='When used with log, shows num_entries number of block entries', required=False)
    parser.add_argument('-y', '--why', type=str, help='Reason for the removal of the evidence item', required=False)
    parser.add_argument('-r', '--reverse', type=bool, help="Reverses the order of the block entries to show the most recent entries first", required=False)
    parser.add_argument('-o', type=str, help='Information about the lawful owner to whom the evidence was released', required=False)
    
    # Parse the arguments passed to the program
    args = parser.parse_args()
    
    '''
    A more verbose method of doing variable assignment
    while we could just do so in the argument parsing.
    '''
    # [Bool] vars, positional args
    checkout = args.checkout
    checkin = args.checkin
    remove = args.remove
    verify = args.verify
    init = args.init
    add = args.add
    log = args.log
    
    # Actual value variables, optional args
    num_entries = args.n        # int
    case_id = args.c            # String, need to conv to UUID
    item_id = args.i            # int
    reverse = args.reverse      # bool, usually paired with n?
    reason = args.why           # str
    owner = args.o              # str
    
    if checkout:
        '''
        requires:
        
        returns:
            
        '''
    elif checkin:
        '''
        requires:
        
        returns:
            
        '''
    elif remove:
        '''
        requires:
        
        returns:
            
        '''
    elif verify:
        '''
        requires:
        
        returns:
            
        '''
    elif init:
        '''
        requires:
        
        returns:
            
        '''
    elif add:
        '''
        requires:
        
        returns:
            
        '''
    elif log:
        '''
        requires:
        
        returns:
            
        '''
    else:
        parser.print_help()
        sys.exit(0)
    
# Start off main
if __name__ == '__main__':
    main()




