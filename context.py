#!/usr/bin/env python
import argparse
import os
import sys

from context import Contexts

def context(args):
    """
    Context functionality from __main__

    This will get the global contexts object and run some basic system commands
    """
    contexts = load_contexts(args.contexts_file, options=args)

    if not args.command:
        contexts.help()
        sys.exit(0)

    try:
        contexts.run_command(args.command, args)
    except Exception, e:
        sys.stderr.write("%s\n" % e.message)

def load_contexts(data_file="~/.contexts", options={}):
    """Load the contexts file and create the Contexts object"""
    data_file = os.path.expanduser(data_file)
    data = None

    # if the data file exists, load that
    if os.path.exists(data_file):
        data = open(data_file, 'r').read()

    context = Contexts(data, options=options)
    return context

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Context switcher')
    # add arguments
    parser.add_argument('command', help='Choose your command', nargs="?")
    parser.add_argument('subcommand', help='Choose your sub commands', nargs="*")
    parser.add_argument('--contexts', '-c', help="The contexts data file", action="store", dest="contexts_file", default="~/.contexts")
    parser.add_argument('--data', '-d', help="The contexts library data file", action="store", dest="data_file", default="~/.contexts_data")
    parser.add_argument('--verbose', '-v', help="Show more information about process", dest="verbose", action="store_true", default=False)
    args = parser.parse_args()
    context(args)
