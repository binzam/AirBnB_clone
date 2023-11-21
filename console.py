#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import shlex
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HBNB command interpreter."""

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        return True

    def do_quit(self, line):
        """Quits command to exit the program."""
        return True

    def emptyline(self):
        """Prevents resoponse to empty line"""
        pass

    def do_create(self, arg):
        """Creates a new instances of BaseModel saves
        it to the JSON file and prints the id.
        """
        if not arg:
            print("** class name missing **")
            return
        try:
            model = eval(arg)()
            model.save()
            print(model.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id.
        """
        arg = shlex.split(arg)
        if not arg:
            print("** class name missing **")
            return
        elif arg[0] not in globals():
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:
            print("** instance id missing **")
            return
        else:
            objs = models.storage.all()
            key = arg[0] + "." + arg[1]
            if key in objs:
                print(objs[key])
            else:
                print("** no instance found **")
                return

    def do_destroy(self, arg):
        """
        Deletes a class based on name and id
        save the change into the JSON file.
        """
        arg = arg.split()
        if not arg:
            print("** class name missing **")
            return
        elif arg[0] not in globals():
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:
            print("** instance id missing **")
            return
        else:
            objs = models.storage.all()
            key = arg[0] + "." + arg[1]
            if key in objs:
                del objs[key]
                models.storage.save()
            else:
                print("** no instance found **")
                return

    def do_all(self, arg):
        """
        Prints string representation of all instances based on class name.
        If no class is specified, displays all instantiated objects
        """
        instances = []
        storage = FileStorage()
        storage.reload()
        objs = storage.all()
        try:
            if len(arg) != 0:
                eval(arg)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, value in objs.items():
            if len(arg) != 0:
                if isinstance(value, eval(arg)):
                    instances.append(str(value))
            else:
                instances.append(str(value))
        print("[", end="")
        print(", ".join(instances), end="")
        print("]")

    def do_update(self, arg):
        """
        Updates a class instance based on a given class name and id by adding
        or updating attribute.
        save the change into the JSON file.
        """
        objs = models.storage.all()
        arg = shlex.split(arg)
        if not arg:
            print("** class name missing **")
            return
        elif arg[0] not in globals():
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:
            print("** instance id missing **")
            return
        else:
            key = arg[0] + "." + arg[1]
            if key not in objs:
                print("** no instance found **")
                return
            elif len(arg) < 3:
                print("** attribute name missing **")
                return
            elif len(arg) < 4:
                print("** value missing **")
                return
            else:
                try:
                    attr_type = type(getattr(objs[key], arg[2]))
                    arg[3] = attr_type(arg[3])
                except AttributeError:
                    pass
                setattr(objs[key], arg[2], arg[3])
                objs[key].save()

    def do_count(self, arg):
        """Counts the number of instances of a given class."""
        instances = []
        storage = FileStorage()
        storage.reload()
        objs = storage.all()
        try:
            if len(arg) != 0:
                eval(arg)
        except NameError:
            print("** class doesn't exist **")
            return
        for key, value in objs.items():
            if len(arg) != 0:
                if isinstance(value, eval(arg)):
                    instances.append(value)
            else:
                instances.append(value)
        print(len(instances))

    def default(self, arg):
        """Default behavior for the cmd module when input is not valid."""
        funcs = {
            "all": self.do_all,
            "update": self.do_update,
            "destroy": self.do_destroy,
            "show": self.do_show,
            "count": self.do_count,
        }
        arg = (
            arg.replace("(", ".")
            .replace(")", ".")
            .replace('"', "")
            .replace(",", "")
            .split(".")
        )
        try:
            key = arg[0] + " " + arg[2]
            func = funcs[arg[1]]
            func(key)
        except Exception:
            pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
