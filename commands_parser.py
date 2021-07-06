# checks if a given command is in the list or not
# list of commands
def swap(list, pos1, pos2):

    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


commands = ["add", "remove", "set", "join", "delete"]


def is_command(command):
    if command in commands:
        return 1
    else:
        return 0


def is_command_add(command):
    if(is_command(command) and command == "add"):
        return 1
    else:
        return 0


def is_command_join(command):
    if(is_command(command) and command == "join"):
        return 1
    else:
        return 0


def is_command_delete(command):
    if(is_command(command) and command == "delete"):
        return 1
    else:
        return 0


def is_command_set(command):
    if(is_command(command) and command == "set"):
        return 1
    else:
        return 0
