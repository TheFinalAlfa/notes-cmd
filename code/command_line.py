import argparse, readline
from .db_modifications import *


    
parser = argparse.ArgumentParser(description="Notes app")

subparsers = parser.add_subparsers(dest="command")

parser_new = subparsers.add_parser("new", help="Adds new note", 
                                   description="""Adds new note to DB. If caption is empty, 
                                   enters dynamic input.""")
parser_new.add_argument("-d", "--dynamic", action="store_true", help="Enters dynamic input mode")
parser_new.add_argument("caption", nargs="*", help="Text - displayed while showing all notes")
parser_new.add_argument("--content", "-c", nargs="*", 
                        help="Text - hidden while showing all notes. Use \"\\\\\" for new line")

parser_show = subparsers.add_parser("show", help="Shows existing notes - all or by ID", 
                                    description="Shows all notes or Shows note with provided ID")
parser_show.add_argument("id", type=int, nargs="?", help="Optional - displays note by ID")

parser_modify = subparsers.add_parser("modify", help="Modifies existing note ID", 
                                      description="Modifies existing note")
parser_modify.add_argument("id", type=int, help="Note's ID")


parser_delete = subparsers.add_parser("del", help="Deletes note by ID", 
                                      description="Deletes existing note by ID, one or more, doesn't check if it exists")
parser_delete.add_argument("id", type=int, help="One or more note IDs to delete", nargs="+")


def dynamic_input(prompt, *prefill: list) -> str:
    ## Args form: (prompt, prefill)
    result = []
    i = 0
    print("Entered dynamic input mode: \nTo exit enter a blank row")
    print(prompt, end="")
    try:
        while True:
            if i < len(prefill):
                readline.set_startup_hook(lambda: readline.insert_text(prefill[i]))
            else:
                readline.set_startup_hook()
            result.append(input())
            if result[-1] == "":
                return "\n".join(result)
            else:
                i += 1
    finally:
        readline.set_startup_hook()

def parse_new(arguments):
    details = {
        "caption" : " ".join(arguments["caption"]),
        "content" : "", 
        }
    
    if arguments["dynamic"]:
        details["caption"] = dynamic_input(["Caption: ", details["caption"]])
    elif details["caption"] == "":
        print("Caption is required")
        return
    # Maybe add a check of details["caption"] value (ex. "\n", ", ', ;)
    
    if isinstance(arguments["content"], list):
        details["content"] = " ".join(arguments["content"])
        details["content"].replace("\\\\", "\n")
    if arguments["dynamic"]:
        details["content"] = dynamic_input()
    
    print("Added note ID: " + str(add_note(details["caption"], details["content"], 
                                           connection).fetchone()[0]))


def parse_show(arguments):
    if "id" in arguments.keys():
        if exists_id(arguments["id"], connection):
            a = get_note_by_id(arguments["id"], connection)
            print(f" ID: {str(a[0])} \n Caption: {a[1]} \n\n{'' if a[2] == 'None' else a[2]}")
        else:
            print("ID not in database")
    else:
        print("Showing all notes \n id \t caption")
        for iteam in get_notes_simple(connection):
            print(f" {str(iteam[0])} \t {iteam[1]}")


def parse_modify(arguments):
    if not exists_id(arguments["id"], connection):
        print("ID not in database")
    else:
        print(f"Modifying note ID: {arguments['id']}")
        note = list(get_note_by_id(arguments["id"], connection))
        # [id, "caption", "content"]
        print(note)
        
        note[1] = rl_input("New caption:\n", note[1])
        note[2] = rl_input("New content: \n", note[2])
        update_note(note[0], note[1], note[2], connection)


def parse_del(arguments):
    for i in arguments["id"]:
        delete_note(i, connection)
    print(f"Deleted notes with IDs: {str(arguments['id'])}")


def parse_arguments(parser, connection:sqlite3.Connection):
    arguments = vars(parser.parse_args())
    
    if arguments["command"] == "new":
        parse_new(arguments)
    elif arguments["command"] == "show" or arguments["command"] == None:
        parse_show(arguments)
    elif arguments["command"] == "modify":
        parse_modify(arguments)
    elif arguments["command"] == "del":
        parse_del(arguments)