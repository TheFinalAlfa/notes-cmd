import argparse, readline
from .db_modifications import *


    
parser = argparse.ArgumentParser(description="Notes app")

subparsers = parser.add_subparsers(dest="command")

parser_new = subparsers.add_parser("new", help="Adds new note", description="""Adds new note to DB. If caption is empty, 
                                   enters dynamic input""")
parser_new.add_argument("caption", nargs="*", help="Text - displayed while showing all notes")
parser_new.add_argument("--content", "-c", nargs="*", help="Text - hidden while showing all notes")

parser_show = subparsers.add_parser("show", help="Shows existing notes - all or by ID", 
                                    description="Shows all notes or Shows note with provided ID")
parser_show.add_argument("id", type=int, nargs="?", help="Optional - displays note by ID")

parser_modify = subparsers.add_parser("modify", help="Modifies existing note ID", description="Modifies existing note")
parser_modify.add_argument("id", type=int, help="Note's ID")


parser_delete = subparsers.add_parser("del", help="Deletes note by ID", 
                                      description="Deletes existing note by ID, one or more, doesn't check if it exists")
parser_delete.add_argument("id", type=int, help="One or more note IDs to delete", nargs="+")


def rl_input(prompt, prefill=""):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()



def parse_arguments(parser, connection:sqlite3.Connection):

    arguments = vars(parser.parse_args())
    
    if arguments["command"] == "new":
        if arguments["caption"] == []:
            details = []
            details.append(input("Caption: \n"))
            if details[0] == "":
                print("Caption is required")
                return
            details.append(rl_input("\nContent: \n", 
                                    prefill="" if arguments["content"] == None else " ".join(arguments["content"])))
            print("Added note ID: " + str(add_note(details[0], "" if details[1] == "" else details[1], connection).fetchone()[0]))
        else:
            print("Added note ID: " + str(add_note(" ".join(arguments["caption"]), "" 
                     if arguments["content"] == None else " ".join(arguments["content"]), 
                     connection).fetchone()[0]))
            
    elif arguments["command"] == "show":
        if arguments["id"]:
            if exists_id(arguments["id"], connection):
                a = get_note_by_id(arguments["id"], connection)
                print(f" ID: {str(a[0])} \n Caption: {a[1]} \n\n{'' if a[2] == 'None' else a[2]}")
            else:
                print("ID not in database")
        else:
            print("Showing all notes \n id \t caption")
            for iteam in get_notes_simple(connection):
                print(f" {str(iteam[0])} \t {iteam[1]}")
                
    elif arguments["command"] == "modify":
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
    
    elif arguments["command"] == "del":
        print(arguments["id"])
        for i in arguments["id"]:
            delete_note(i, connection)
        print(f"Deleted notes with IDs: {str(arguments['id'])}")
    