#!/usr/bin/python3

import argparse
from code import *

connection = set_up_db("/home/gargamel/Projects/notes/notes_cmd/db.db")

parser = argparse.ArgumentParser(description="Notes app")

construct_parser(parser)

parse_arguments(parser, connection)
