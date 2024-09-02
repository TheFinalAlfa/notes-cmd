import argparse, readline, sqlite3

from .db_modifications import *
from .db_tags import *

def construct_parser_tags(parser:argparse.ArgumentParser, subparsers:dict):
    # Add check if exists "subparsers["command"]"
    if "command" not in subparsers.keys():
        subparsers["command"] = parser.add_subparsers(dest="command")

    parser_tags = subparsers["command"].add_parser("tag", help="Commands regarding tags")
    
    subparsers["tag"] = parser_tags.add_subparsers(dest="tag")
    
    tags_show = subparsers["tag"].add_parser("show")
    
    tags_new = subparsers["tag"].add_parser("new")
    tags_new.add_argument("name")
    
    tags_del = subparsers["tag"].add_parser("del")
    tags_del.add_argument("id", type=int)
    
    tags_modify = subparsers["tag"].add_parser("modify")
    tags_modify.add_argument("id", type=int)
    tags_modify.add_argument("name")

def parse_args_tag(arguments):
    print(arguments)

def parse_tag_new(arguments, connection:sqlite3.Connection):
    new_tag(arguments["name"], connection)