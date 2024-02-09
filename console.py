#!/usr/bin/python3
"""
Command inter-preter for the Air-BnB project.
"""
import cmd
from models import storage, CNC


class HBNBCommand(cmd.Cmd):
    """
    Command Start class.
    """
    prompt = '(hbnb) '
    ERR = [
        '** class name missing **',
        '** class doesn\'t exist **',
        '** instance id missing **',
        '** no instance found **',
        '** attribute name missing **',
        '** value missing **',
        ]

    def preloop(self):
        """
        Handling start to command inter-preter.
        """
        print('.----------------------------.')
        print('|    Welcome to hbnb CLI!    |')
        print('|   for help, input \'help\'   |')
        print('|   for quit, input \'quit\'   |')
        print('.----------------------------.')

    def postloop(self):
        """
        Handling exit of command inter-preter.
        """
        print('.----------------------------.')
        print('|  Well, that sure was fun!  |')
        print('.----------------------------.')

    def default(self, line):
        """
        Default response of unknown comands.
        """
        print("This \"{}\" is invalid, run \"help\" "
              "for more explanations".format(line))

    def emptyline(self):
        """
        At empty line given in response in the prompt.
        """
        pass

    def __class_err(self, arg):
        """
        Checking if missing or unknown class.
        """
        error = 0
        if len(arg) == 0:
            print(HBNBCommand.ERR[0])
            error = 1
        else:
            if isinstance(arg, list):
                arg = arg[0]
            if arg not in CNC.keys():
                print(HBNBCommand.ERR[1])
                error = 1
        return error

    def __id_err(self, arg):
        """
        Checking of missing or unknown id.
        """
        error = 0
        if (len(arg) < 2):
            error += 1
            print(HBNBCommand.ERR[2])
        if not error:
            storage_objs = storage.all()
            for key, value in storage_objs.items():
                temp_id = key.split('.')[1]
                if temp_id == arg[1] and arg[0] in key:
                    return error
            error += 1
            print(HBNBCommand.ERR[3])
        return error

    def do_quit(self, line):
        """Command to quit the program. """
        return True

    def do_EOF(self, line):
        """A Function to handle EOF. """
        print()
        return True

    def __isfloat(self, val):
        """
        Checking string convering to a float.
        """
        try:
            float(val)
            return True
        except:
            return False

    def __update_val(self, v):
        """Updating string to proper type either int float or
        string. """
        if v[0] == '"' and v[-1] == '"':
            v = v[1:-1]
            v = v.replace('"', '\"')
            v = v.replace('_', ' ')
            return v
        if v.isdigit():
            v = int(v)
        elif self.__isfloat(v):
            v = float(v)
        return v

    def __create_dict(self, attr_dict, arg):
        """Creating dictionary from input paramaters of create func. """
        for params in arg:
            if '=' in params:
                i = params.index('=')
                if i < len(params) - 1:
                    k = params[:i]
                    v = params[(i + 1):]
                    v = self.__update_val(v)
                    attr_dict[k] = v
        return attr_dict

    def do_create(self, arg):
        """Creating dictionary from create func. """
        arg = arg.split()
        error = self.__class_err(arg)
        if error:
            return
        k = arg[0]
        class_obj = CNC[k]
        if len(arg) > 1:
            d = self.__create_dict({}, arg[1:])
        else:
            d = {}
        my_obj = class_obj(**d)
        my_obj.save()
        print(my_obj.id)

    def do_show(self, arg):
        """Prints object of given id from given Class. """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            storage_objs = storage.all()
            for k, v in storage_objs.items():
                if arg[1] in k and arg[0] in k:
                    print(v)

    def do_all(self, arg):
        """Prints all objects of given class. 
        """
        arg = arg.split()
        error = 0
        if arg:
            error = self.__class_err(arg)
            if error:
                return
        print('[', end='')
        l = 0
        if arg:
            storage_objs = storage.all(arg[0])
        else:
            storage_objs = storage.all()
        l = len(storage_objs)
        c = 0
        for v in storage_objs.values():
            c += 1
            print(v, end=(', ' if c < l else ''))
        print(']')

    def do_destroy(self, arg):
        """Destroying object of given ID from given Class. 
        """
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if error:
            return
        storage_objs = storage.all()
        for k in storage_objs.keys():
            if arg[1] in k and arg[0] in k:
                to_delete = storage_objs[k]
        to_delete.delete()
        storage.save()

    def __rremove(self, s, l):
        """
        Removes characters in the input list from input string. 
        """
        for c in l:
            s = s.replace(c, '')
        return s

    def __check_dict(self, arg):
        """
        Checks if the arguments input has a dictionary. 
        """
        if '{' and '}' in arg:
            l = arg.split('{')[1]
            l = l.split(', ')
            l = list(s.split(':') for s in l)
            d = {}
            for subl in l:
                k = subl[0].strip('"\' {}')
                v = subl[1].strip('"\' {}')
                d[k] = v
            return d
        else:
            return None

    def __handle_update_err(self, arg):
        """
        Checks for all errors in update. 
        """
        d = self.__check_dict(arg)
        arg = self.__rremove(arg, [',', '"'])
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if error:
            return [0]
        valid_id = 0
        storage_objs = storage.all()
        for k in storage_objs.keys():
            if arg[1] in k and arg[0] in k:
                key = k
        if len(arg) < 3:
            print(HBNBCommand.ERR[4])
        elif len(arg) < 4:
            print(HBNBCommand.ERR[5])
        else:
            return [1, arg, d, storage_objs, key]
        return [0]

    def do_update(self, arg):
        """Updates or adds a new attribute and value of given Class. 
        """
        arg_inv = self.__handle_update_err(arg)
        if arg_inv[0]:
            arg = arg_inv[1]
            d = arg_inv[2]
            storage_objs = arg_inv[3]
            key = arg_inv[4]
            if not d:
                avalue = arg[3].strip('"')
                if avalue.isdigit():
                    avalue = int(avalue)
                storage_objs[key].bm_update({arg[2]: avalue})
            else:
                for k, v in d.items():
                    if v.isdigit():
                        v = int(v)
                    storage_objs[key].bm_update({k: v})

    def do_BaseModel(self, arg):
        """class method with function syn. """
        self.__parse_exec('BaseModel', arg)

    def do_Amenity(self, arg):
        """class method with function syn. """
        self.__parse_exec('Amenity', arg)

    def do_City(self, arg):
        """class method with function syn. """
        self.__parse_exec('City', arg)

    def do_Place(self, arg):
        """class method with function syn. """
        self.__parse_exec('Place', arg)

    def do_Review(self, arg):
        """class method with function syn. """
        self.__parse_exec('Review', arg)

    def do_State(self, arg):
        """class method with function syn. """
        self.__parse_exec('State', arg)

    def do_User(self, arg):
        """class method with function syn. """
        self.__parse_exec('User', arg)

    def __count(self, arg):
        """Counting no of objects in File-Storage. """
        args = arg.split()
        storage_objs = storage.all()
        count = 0
        for k in storage_objs.keys():
            if args[0] in k:
                count += 1
        print(count)

    def __parse_exec(self, c, arg):
        """
        Parses the input from .function() syntax, calls matched func.
        """
        CMD_MATCH = {
            '.all': self.do_all,
            '.count': self.__count,
            '.show': self.do_show,
            '.destroy': self.do_destroy,
            '.update': self.do_update,
            '.create': self.do_create,
        }
        if '(' and ')' in arg:
            check = arg.split('(')
            new_arg = "{} {}".format(c, check[1][:-1])
            for k, v in CMD_MATCH.items():
                if k == check[0]:
                    if ((',' or '"' in new_arg) and k != '.update'):
                        new_arg = self.__rremove(new_arg, ['"', ','])
                    v(new_arg)
                    return
        self.default(arg)

if __name__ == '__main__':
    """
    MAIN Loop
    """
    HBNBCommand().cmdloop()
