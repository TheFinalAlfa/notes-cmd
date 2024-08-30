#!/usr/bin/python3

import argparse
from code import *

connection = set_up_db("/home/gargamel/Projects/notes/notes_cmd/db.db")

parser = argparse.ArgumentParser(description="Notes app")
subparsers_command = parser.add_subparsers(dest="command")

construct_parser_base(parser, subparsers_command)

parse_arguments(parser, connection)
