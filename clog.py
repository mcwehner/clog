#!/usr/bin/env python

import sys
import yaml

from optparse import OptionParser

from clog.client import Client, ClientError


def parse_options():
    help = [
        'Usage: %prog [options] <command>',
        '',
        'Commands:',
    ]
    
    help.extend(['  %s' % c for c in Client.command_list()])
    
    parser = OptionParser( '\n'.join(help) )
    
    parser.add_option(
        '-v', '--verbose', dest='verbose', action='store_true',
        help='More verbose output',
    )
    
    parser.add_option(
        '--text_to_speech', dest='text_to_speech', action='store_true',
        help="Use the shell `say' command to enable text-to-speech for messages",
    )
    
    parser.add_option(
        '-l', '--live', dest='live', action='store_true',
        help='Use the "live" chat stream instead of transcript polling',
    )
    
    options, args = parser.parse_args()
    
    if not args:
        parser.print_usage()
        sys.exit(1)
    
    return options, args


def main():
    options, args = parse_options()
    
    try:
        subdomain  = None
        auth_token = None
        command    = args.pop(0)
        
        with open('credentials.yaml') as fh:
            credentials = yaml.load(fh)
            subdomain   = credentials['subdomain']
            auth_token  = credentials['auth_token']
            
        client = Client(subdomain, auth_token)
        
        client.call_command(command, *args, **options.__dict__)
        
    except ClientError, e:
        sys.stderr.write(e.message)
        sys.exit(1)


if '__main__' == __name__:
    main()
