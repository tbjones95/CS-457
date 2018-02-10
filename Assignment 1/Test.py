import os
import cmd
from GlobalVars import *

class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "=>> "
        self.intro  = "Welcome to console!"  ## defaults to None

    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    ## Command definitions ##
    def do_CREATE(self, cmd):
        print cmd

        if cmd == "TABLE":
            print "Database created"
        elif cmd.startswith(CREATE_DATABASE):
            print "Table created"

    def do_EXIT(self, cmd):

        return -1

if __name__ == '__main__':
        console = Console()
        console . cmdloop()
