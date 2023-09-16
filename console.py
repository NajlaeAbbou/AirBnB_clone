#!/usr/bin/python3
"""Console hbnb"""
import re
from shlex import split
import cmd

class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """exit the program"""
        return True

    def do_EOF(self, arg):
        """exit the program"""
        print("")
        return True

     def emptyline(self):
        """empty line + ENTER"""
        pass

    if __name__ == "__main__":
    HBNBCommand().cmdloop()



