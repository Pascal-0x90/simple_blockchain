# -*- coding: utf-8 -*-

import argparse
import uuid # For the case id. Probably used in the caseID module
import sys
import linkedlist
import block_chain
import os

DEBUG = True # Set to true for verbosity of main

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
    subparsers =parser.add_subparsers(help='sub-command help')

    parser_add=subparsers.add_parser('add',help='Add a new evidence item to the blockchain and associate it with the given case identifier')
    parser_add.add_argument('-c', type=str, metavar='CASE_ID', help='Specifies the case identifier that the evidence is associated with', required=True)
    parser_add.add_argument('-i', type=int, action='append', metavar='ITEM_ID [-i ITEM_ID ...]',help='Specifies the evidence item’s identifier', required=True)
    parser_add.set_defaults(which='add')

    parser_checkout=subparsers.add_parser('checkout',help='Add a new evidence item to the blockchain and associate it with the given case identifier')
    parser_checkout.add_argument('-i', type=str, metavar='ITEM_ID', help='Specifies the item identifier that the evidence is associated with', required=True)
    parser_checkout.set_defaults(which='checkout')

    parser_checkin=subparsers.add_parser('checkin',help='Add a new checkin entry to the chain of custody for the given evidence item')
    parser_checkin.add_argument('-i', type=str,metavar='ITEM_ID', help='Specifies the item identifier that the evidence is associated with', required=True)
    parser_checkin.set_defaults(which='checkin')

    parser_log=subparsers.add_parser('log',help='Display the blockchain entries giving the oldest first (unless -r is given)')
    parser_log.add_argument('-r', '--reverse', type=bool, help="Reverses the order of the block entries to show the most recent entries first", required=False)
    parser_log.add_argument('-n', type=int, help='When used with log, shows num_entries number of block entries', required=False)
    parser_log.add_argument('-c', type=str, metavar='CASE_ID', help='Specifies the case identifier that the evidence is associated with', required=False)
    parser_log.add_argument('-i', type=int, nargs=1,action='store', metavar='ITEM_ID',help='Specifies the evidence item’s identifier', required=False)
    parser_log.set_defaults(which='log')


    parser_remove=subparsers.add_parser('remove',help='Prevents any further action from being taken on the evidence item specified')
    parser_remove.add_argument('-i', type=int, nargs=1,action='store', metavar='ITEM_ID',help='Specifies the evidence item’s identifier', required=True)
    parser_remove.add_argument('-y', '--why', type=str, help='Reason for the removal of the evidence item',choices=['RELEASED', 'DISPOSED', 'DESTROYED'], required=True)
    parser_remove.add_argument('-o', type=str,metavar='Owner', help='Information about the lawful owner to whom the evidence was released', required=(('-y' in sys.argv and 'RELEASED' in sys.argv) or ('--why' in sys.argv and 'RELEASED' in sys.argv)))
    parser_remove.set_defaults(which='remove')

    parser_init=subparsers.add_parser('init', help='Sanity check. Only starts up and checks for the initial block')
    parser_init.set_defaults(which='init')

    parser_verify=subparsers.add_parser('verify', help='Parse the blockchain and validate all entries')
    parser_verify.set_defaults(which='verify')


    # Parse the arguments passed to the program
    args = parser.parse_args()
    
    if DEBUG:
        print(args)
    
    # Check if we have args, if not then show help and exit
    try:
        option = args.which
    except AttributeError:
        parser.print_help()
        sys.exit(0)

    #get the blockchain object
    bc_obj = block_chain.blockchain()
    # Obtain or init block chain at each run
    if option != 'init':
        # Check but no printout
        bc_obj.init(True)

    # Begin our case statements
    if option == 'checkout':
        #if its CHECKEDOUT then checkout() will fail, aka it will have ot be CHECKEDIN to succeed
        item_id = int(args.i)
        if DEBUG:
            print(type(item_id))
            print('action chosen was checkout')

        #find a block with the same item_id
        prev_block = bc_obj.search_by_id(item_id)
        if prev_block is None:
            #print and error that we did not find a block with that item_id?
            if DEBUG:
                print('DID NOT FIND THE BLOCK WITH THAT ITEM_ID')
        else:
            #call get the current state of this item and check that the current state is CHECKEDIN
            current_state = bc_obj.get_curr_state_of_item(item_id)
            if DEBUG:
                print(current_state)
            if current_state == "CHECKEDIN":

                bc_obj.checkout(item_id, prev_block.case_id)

            elif current_state == "CHECKEDOUT":
                print('Error: Cannot check out a checked out item. Must check it in first.')
        


    elif option == 'checkin':
        #if its DESTROYED, DISPOSED, RELEASED, or CHECKEDOUT then checkout() will fail, aka it will have ot be CHECKEDIN to succeed
        item_id = int(args.i)
        if DEBUG:
            print(type(item_id))
            print('action chosen was checkin')
        prev_block = bc_obj.search_by_id(item_id)
        if prev_block is None:
            #print and error that we did not find a block with that item_id?
            if DEBUG:
                print('DID NOT FIND THE BLOCK WITH THAT ITEM_ID')
        else:
            #call get the current state of this item and check that the current state is CHECKEDIN
            current_state = bc_obj.get_curr_state_of_item(item_id)
            if DEBUG:
                print(current_state)
            if current_state == "CHECKEDOUT":
                
                bc_obj.checkin(item_id, prev_block.case_id)

            elif current_state == "CHECKEDIN":
                #print error if checked in item?
                #print('Error: Cannot check in a checked in item. Must check it out first.')
                pass
        
    elif option == 'remove':
        if DEBUG:
            print('action chosen was remove')
        item_id = int(args.i[0])            # int
        reason = args.why           # str
        try:
            owner = args.o              # str
        except:
            owner = False    
        current_state = bc_obj.get_curr_state_of_item(item_id)
        if DEBUG:
            print(current_state)
        prev_block = bc_obj.search_by_id(item_id)
        if current_state is None:
            #print and error that we did not find a block with that item_id?
            pass
        elif current_state == "CHECKEDIN":
            bc_obj.remove(item_id, prev_block.case_id, reason, owner)
        else:
            if DEBUG:
                print('Error: Cannot remove an item not checked in.')
            



    elif option == 'verify':
        if DEBUG:
            print('action chosen was verify')
        '''
        requires:
        
        returns:
            
        '''
        bc_obj.verify()
    elif option == 'init':
        if DEBUG:
            print('action chosen was init')
        # Since it is already init'd, we can just export
        bc_obj.init()

    elif option == 'add':
        if DEBUG:
            print('action chosen was add')
        #please remember that this is the only option where ITEM_ID can be represented as a list, rather than just an int
        case_id = args.c            # String, need to conv to UUID
        item_id = args.i            # int or List
        ####
        ####THIS makes sure that there are no items in the blockchain that have the same item id, 
        ####if any of the given items do the program exits
        ####
        for item in item_id:
            test = bc_obj.search_by_id(item)
            if test!=None:
                sys.exit(0)
        ####
        ####
        ####
        bc_obj.new_evidence_add(case_id, item_id)

    elif option == 'log':
        if DEBUG:
            print('action chosen was log')
        #the arguments for log are all optional, use TRY to see if theyre given.
        try:
            num_entries = args.n        # int
        except:
            num_entries = False
        try:
            case_id = args.c            # String, need to conv to UUID
        except:
            case_id = False
        try:
            item_id = args.i            # int
        except:
            item_id = False
        try:
            reverse = args.reverse      # bool, usually paired with n?
        except:
            reverse = False


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




