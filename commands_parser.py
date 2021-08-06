# checks if a given command is in the list or not
# list of commands
# checking if a given command is in list, and returns false if not
# swap function
def swap(list, pos1, pos2):

    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


# list of all commands
commands = ["add", "remove", "set", "join", "delete", "list", "help", "rename", "describe"]


def is_command(command):  # hell bello
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


def is_command_list(command):
    if(command[0:4] == "list"):
        return 1
    else:
        return 0


def is_command_help(command):
    if(is_command(command) and command == "help"):
        return 1
    else:
        return 0


def is_command_rename(command):
    if(is_command(command) and command == "rename"):
        return 1
    else:
        return 0

def is_command_describe(command):
    if(is_command(command) and command == "describe"):
        return 1
    else:
        return 0