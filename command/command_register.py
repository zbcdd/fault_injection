class CommandRegister(dict):
    def __init__(self, *args, **kwargs):
        super(CommandRegister, self).__init__(*args, **kwargs)
        self._dict = {}

    def __call__(self, command_name):
        def add_command(command_class):
            if not command_name:
                raise Exception(f'command name must be specified! But received command: {command_name}')
            if command_name in self._dict:
                raise Exception(f'command {command_name} has been registered before.')
            self._dict[command_name] = command_class
            return command_class

        return add_command

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()


command_register = CommandRegister()
