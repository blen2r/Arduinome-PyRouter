import cmd
import time
import os
import imp

class CLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.ruler = ""
        self.prompt = "> "
        
        self.__modules = {} #can't use a command's name or a command's option's name as a key
    
    def do_create(self,  args):
        args = args.split(" ")
        
        if len(args) != 2:
            print "Error! Not enough or too many arguments... See \"help create\" for details"
            print
            return
        
        if not args[0] in self.listModules():
            print "Error! Unknown module type See \"list modules\" for a list of available modules"
            print
            return
        
        if args[1] in self.__modules.keys():
            print "Error! This object's name already exists... See \"list objects\" for a list of unusable names"
            print
            return
        
        py_mod = imp.load_source(args[0], "modules/"+args[0]+".py")
        #allo = py_mod.OscIn()
        #test = eval("py_mod."+args[0]+"()")
        self.__modules[args[1]] = [eval("py_mod."+args[0]+"()"),  args[0]]
        
        
    def help_create(self): #cree un module
        print "Creates a module"
        print
        print "    usage: \"create <ModuleType> <objectName>\""
        print "    where <ModuleType> is the type of module to create (you can view a list of available modules by typing: \"list modules\")"
        print "    and where <objectName> is an unused object name for your new object (you can view a list of all the current objects by typing: \"list objects\")."
        print
    
    def do_delete(self,  args):
        pass
    
    def help_delete(self):
        print "Deletes a module"
        print
        print "    usage: \"delete <objectName>\""
        print "    where <objectName> is the name of the object to delete (you can view a list of all the current objects by typing: \"list objects\")."
        print
    
    def do_list(self,  args):
        args = args.split(" ")
        
        if len(args[0]) < 1:
            print "Error! Not enough arguments... See \"help list\" for details"
            print
            return
        
        if args[0] == "run":
            if len(args) < 2:
                print "Error! Not enough arguments... See \"help list\" for details"
                print
            try:
                self.__modules[args[1]].listRunnables()
            except KeyError:
                print "Error! No object named \"" + args[1] + "\"..."
                print
                
        elif args[0] == "objects":
            theKeys = self.__modules.keys()
            theKeys.sort()
            if theKeys is None:
                print "No objects were created yet..."
            else:
                print "Name    |    Type"
                print "-----------------"
                for key in theKeys:
                    print  key + "        " + self.__modules[key][1]
                    print "-----------------"
            print
            
        elif args[0] == "modules":
            mod = self.listModules()
            if len(mod) > 0:
                print "Available modules:"
                j = 0
                for i in mod:
                    print "    " + i #+ "creation arguments: "+ creaArgs[j]
                    j = j+1
                print
            else:
                print "No available modules..."
                print
        
        else:
            print "Error! Unknown option... See \"help list\" for details"
            print
    
    def listModules(self):
        files = os.listdir("modules")
        mod = []
        allArgs = []
        
        for f in files:
            if f.endswith(".py"):
                fs = file("modules/"+f,  "r")
                line1 = fs.readline()
#                args = ""
#                
#                for i in fs: #finds args for __init__
#                    j = i.strip()
#                    print j
#                    if j.startswith("def __init__("):
#                        args=j.split("def __init__(")[1].split(")")[0]
                
                fs.close()
                if line1[:-1] == "#import 1":
                    mod.append(f.split(".py")[0])
                    #allArgs.append(args)
        
        return mod#,  allArgs
                
    
    def help_list(self): #liste les objets existants et les methodes pouvant etre appelees ainsi que les modules pouvant etre crees
        print "Displays a list of the wanted type"
        print
        print "    usage: \"list <type> [<object>]\""
        print "    whith the following options:"
        print "    <type> = run"
        print "        lists all the runnable methods of <object>"
        print
        print "    <type> = objects"
        print "        lists all the created objects"
        print
        print "    <type> = modules"
        print "        lists all the modules that can be created"
        print
    
    def do_run(self,  args):
        pass
    
    def help_run(self): #appelle une methode d'un objet
        print "Runs an object's method"
        print
        print "    usage: \"run <object> [<arg1>[,<arg2>[,<...>]]]\""
        print "    where <object> is the selected object and <arg1>, <arg2> and <...> are the arguments to pass to the method."
        print "    Note: you MUST pass the arguments when needed. You can view details of a command via the \"list\" command (see \"help list\")"
        print
    
    def do_save(self,  args):
        pass
    
    def help_save(self):
        print "Saves the current status (objets, links, ...) to the selected file"
        print
        print "    usage: save <path_to_file>"
        print "    where <path_to_file> is the file you want to save to. You should respect your operating system's path name convention."
        print
    
    def do_load(self,  args):
        pass
    
    def help_load(self):
        print "Loads a status (objets, links, ...) from the selected file"
        print
        print "    usage: load <path_to_file>"
        print "    where <path_to_file> is the file you want to load. You should respect your operating system's path name convention."
        print
        
    def emptyline(self):
        pass
    
    def help_help(self):
        print "Displays the help file"
        print
    
    def can_exit(self):
        return True
    
    def do_exit(self, args):
        print
        print "Please wait 10 seconds for the sockets' automatic shutdown..."
        return True
    
    def help_exit(self):
        print "Exits the application without saving your changes"
        print

if __name__ == "__main__":
    cli = CLI()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        cli.do_exit(None)
