import argparse, readline

from .db_modifications import *


def construct_parser_tags(parser:argparse.ArgumentParser, subparsers_command):
    parser_tags = subparsers_command.add_parser("tags", help="Commands regarding tags")
    subparsers_tags = parser_tags.add_subparsers(dest="tag")
    
    tags_show = subparsers_tags.add_parser("show")
    
    tags_new = subparsers_tags.add_parser("new")
    tags_new.add_argument("name")
    
    tags_del = subparsers_tags.add_parser("del")
    tags_del.add_argument("id", type=int)
    
    tags_modify = subparsers_tags.add_parser("modify")
    tags_modify.add_argument("id", type=int)
    tags_modify.add_argument("name")