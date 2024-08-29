#!/usr/bin/python3

from code import *

connection = set_up_db("/home/gargamel/Projects/notes/notes_cmd/db.db")

parse_arguments(parser, connection)
