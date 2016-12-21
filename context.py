#!/usr/bin/env python
import argparse
import os
import sys
import pprint
import traceback

from context import Contexts


def context(args, remaining_args):
    """
    Context functionality from __main__

    This will get the global contexts object and run some basic system commands
    """
    contexts = load_contexts(args.contexts_file, options=args)

    if not args.command:
        contexts.help()
        sys.exit(0)

    try:
        contexts.run_command(args.command, args, remaining_args)
    except Exception as e:
        sys.stderr.write("%s\n" % e)
        pp = pprint.PrettyPrinter(stream=sys.stderr)
        pp.pprint(e)
        traceback.print_exc(file=sys.stderr)


def load_contexts(data_file="~/.contexts", options={}):
    """Load the contexts file and create the Contexts object"""
    data_file = os.path.expanduser(data_file)
    data = None

    # if the data file exists, load that
    if os.path.exists(data_file) and os.path.isfile(data_file):
        data = open(data_file, 'r').read()
    # the context data is a directory, not a file
    elif os.path.exists(data_file) and os.path.isdir(data_file):
        data = []
        for context_file in os.listdir(data_file):
            this_path = "%s/%s" % (data_file, context_file)
            filename, file_extension = os.path.splitext(this_path)
            if file_extension == '.json':
                # add this data
                data.append(open(this_path, 'r').read())

    context = Contexts(data, options=options)
    return context

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Context switcher')
    # add arguments
    parser.add_argument('command', help='Choose your command', nargs="?")
    parser.add_argument(
        'subcommand',
        help='Choose your sub commands',
        nargs="*")
    parser.add_argument(
        '--context',
        '-t',
        help="Provide an alternate context to perform action against",
        action="store",
        dest="context",
        default=None
    )
    parser.add_argument(
        '--contexts',
        '-c',
        help="The contexts data file",
        action="store",
        dest="contexts_file",
        default="~/.contexts")
    parser.add_argument(
        '--data',
        '-d',
        help="The contexts library data file",
        action="store",
        dest="data_file",
        default="~/.contexts_data")
    parser.add_argument(
        '--verbose',
        '-v',
        help="Show more information about process",
        dest="verbose",
        action="store_true",
        default=False)
    parser.add_argument(
        '--project',
        '-p',
        help="Run commands against a sub-project",
        dest="project",
        action="store",
    )
    args, remaining = parser.parse_known_args()
    context(args, remaining)
