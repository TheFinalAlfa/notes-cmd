import argparse, sqlite3
from .command_line_base import construct_parser_base, parse_arguments_base
from .command_line_tags import construct_parser_tags, parse_args_tag


def construct_parser(parser:argparse.ArgumentParser):
    subparsers = dict()
    construct_parser_base(parser, subparsers)
    construct_parser_tags(parser, subparsers)

def parse_arguments(parser, connection:sqlite3.Connection):
    arguments = vars(parser.parse_args())
    
    parse_arguments_base(arguments)
    