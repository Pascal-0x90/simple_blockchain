# -*- coding: utf-8 -*-

import argparse
import uuid # For the case id. Probably used in the caseID module
import sys
import linkedlist
import block_chain
import os

DEBUG = False # Set to true for verbosity of main

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
    parser_checkout.add_argument('-c', type=str, metavar='CASE_ID', help='Specifies the case identifier that the evidence is associated with', required=True)
    parser_checkout.set_defaults(which='checkout')

    parser_checkin=subparsers.add_parser('checkin',help='Add a new checkin entry to the chain of custody for the given evidence item')
    parser_checkin.add_argument('-c', type=str,metavar='CASE_ID', help='Specifies the case identifier that the evidence is associated with', required=True)
    parser_checkin.set_defaults(which='checkin')

    parser_log=subparsers.add_parser('log',help='Display the blockchain entries giving the oldest first (unless -r is given)')
    parser_log.add_argument('-r', '--reverse', type=bool, help="Reverses the order of the block entries to show the most recent entries first", required=False)
    parser_log.add_argument('-n', type=int, help='When used with log, shows num_entries number of block entries', required=False)
    parser_log.add_argument('-c', type=str, metavar='CASE_ID', help='Specifies the case identifier that the evidence is associated with', required=False)
    parser_log.add_argument('-i', type=int, nargs=1,action='store', metavar='ITEM_ID',help='Specifies the evidence item’s identifier', required=False)
    parser_log.set_defaults(which='log')


    parser_remove=subparsers.add_parser('remove',help='Prevents any further action from being taken on the evidence item specified')
    parser_remove.add_argument('-i', type=int, nargs=1,action='store', metavar='ITEM_ID',help='Specifies the evidence item’s identifier', required=True)
    parser_remove.add_argument('-y', '--why', type=str, help='Reason for the removal of the evidence item', required=True)
    parser_remove.add_argument('-o', type=str,metavar='Owner', help='Information about the lawful owner to whom the evidence was released', required=False)
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

    # Begin our case statements
    if option == 'checkout':
        if DEBUG:
            print('action chosen was checkout')
        case_id = args.c            # String
        print(type(case_id))
        '''
        requires:
        
        returns:
            
        '''
    elif option == 'checkin':
        if DEBUG:
            print('action chosen was checkin')
        case_id = args.c            # String
        '''
        requires:
        
        returns:
            
        '''
    elif option == 'remove':
        if DEBUG:
            print('action chosen was remove')
        item_id = args.i            # int
        reason = args.why           # str
        try:
            owner = args.o              # str
        except:
            owner = False             
        '''
        requires:
        
        returns:
            
        '''
    elif option == 'verify':
        if DEBUG:
            print('action chosen was verify')
        '''
        requires:
        
        returns:
            
        '''
    elif option == 'init':
        if DEBUG:
            print('action chosen was init')
        if os.path.exists(bc_obj.file_path):
            bc_obj.import_bc()
            #find the init block
            wasFound = bc_obj.search_by_id(0)

            #
            if wasFound:
                print('Blockchain file found with INITIAL block.')
            else:
                if DEBUG:
                    print('imported but did not find init block')
        else:
            #call the init funciton
            bc_obj.init()
            # Write to file
            bc_obj.export_bc()
            
            print('Blockchain file not found. Created INITIAL block.')

    elif option == 'add':
        if DEBUG:
            print('action chosen was add')
        #please remember that this is the only option where ITEM_ID can be represented as a list, rather than just an int
        case_id = args.c            # String, need to conv to UUID
        item_id = args.i            # int or List
        '''
        requires:
        
        returns:
            
        '''
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




