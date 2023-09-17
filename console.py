#!/usr/bin/python3

"""Console hbnb"""
import re
from shlex import split
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def analyse(arg):
    accollade = re.search(r"\{(.*?)\}", arg)
    crochets = re.search(r"\[(.*?)\]", arg)
    if accollade is None:
        if crochets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lx = split(arg[:crochets.span()[0]])
            mylt = [i.strip(",") for i in lx]
            mylt.append(crochets.group())
            return (mylt)
    else:
        lx = split(arg[:accollade.span()[0]])
        mylt = [i.strip(",") for i in lx]
        mylt.append(accollade.group())
        return mylt


class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

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

    def default(self, arg):
        """Default behavior"""
        diction = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        kv = re.search(r"\.", arg)
        if kv is not None:
            argss = [arg[:kv.span()[0]], arg[kv.span()[1]:]]
            kv = re.search(r"\((.*?)\)", argss[1])
            if kv is not None:
                cmad = [argss[1][:kv.span()[0]], kv.group()[1:-1]]
                if cmad[0] in diction.keys():
                    cl = "{} {}".format(argss[0], cmad[1])
                    return diction[cmad[0]](cl)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """Create  new class inst,print its id"""
        argss = analyse(arg)
        if len(argss) == 0:
            print("** class name missing **")
        elif argss[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argss[0])().id)
            models.storage.save()

    def do_show(self, arg):
        """Prints string repres ofan inst based on class name and id"""
        argss = analyse(arg)
        diction = models.storage.all()
        if len(argss) == 0:
            print("** class name missing **")
        elif argss[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argss) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argss[0], argss[1]) not in diction:
            print("** no instance found **")
        else:
            print(diction["{}.{}".format(argss[0], argss[1])])

    def do_destroy(self, arg):
        """ Deletes an inst using class name and id"""
        argss = analyse(arg)
        diction = models.storage.all()
        if len(argss) == 0:
            print("** class name missing **")
        elif argss[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argss) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argss[0], argss[1]) not in diction.keys():
            print("** no instance found **")
        else:
            del diction["{}.{}".format(argss[0], argss[1])]
            models.storage.save()

    def do_all(self, arg):
        """Prints all string repr of all inst"""
        argss = analyse(arg)
        if len(argss) > 0 and argss[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            ob = []
            for oj in models.storage.all().values():
                if len(argss) > 0 and argss[0] == oj.__class__.__name__:
                    ob.append(oj.__str__())
                elif len(argss) == 0:
                    ob.append(oj.__str__())
            print(ob)

    def do_update(self, arg):
        """Updates an inst based on class name,id"""
        argss = analyse(arg)
        diction = models.storage.all()

        if len(argss) == 0:
            print("** class name missing **")
            return False
        if argss[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argss) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argss[0], argss[1]) not in diction.keys():
            print("** no instance found **")
            return False
        if len(argss) == 2:
            print("** attribute name missing **")
            return False
        if len(argss) == 3:
            try:
                type(eval(argss[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(argss) == 4:
            ob = diction["{}.{}".format(argss[0], argss[1])]
            if argss[2] in ob.__class__.__dict__.keys():
                tpv = type(ob.__class__.__dict__[argss[2]])
                ob.__dict__[argss[2]] = tpv(argss[3])
            else:
                ob.__dict__[argss[2]] = argss[3]
        elif type(eval(argss[2])) == dict:
            ob = diction["{}.{}".format(argss[0], argss[1])]
            for key, value in eval(argss[2]).items():
                if (key in ob.__class__.__dict__.keys() and
                        type(ob.__class__.__dict__[key]) in {str, int, float}):
                    tpv = type(ob.__class__.__dict__[key])
                    ob.__dict__[key] = tpv(value)
                else:
                    ob.__dict__[key] = value
        models.storage.save()

    def do_count(self, arg):
        """number of instances"""
        argss = analyse(arg)
        c = 0
        for ob in models.storage.all().values():
            if argss[0] == ob.__class__.__name__:
                c += 1
                print(c)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
