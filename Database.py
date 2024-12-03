class Database:
    def __init__(self):
        self.store = {}

    def ApplyCommand(self, command):
        operator = command.split()[0]
        key = command.split()[1]
        value = command.split()[2] if len(command.split()) > 2 else None
        if operator == "SET":
            if value is None:
                return "BAD_COMMAND"
            self.store[key] = value
            return "OK"
        if operator == "GET":
            if key not in self.store:
                return "NOT_FOUND"
            return self.store.get(key)
        if operator == "DEL":
            if key not in self.store:
                return "NOT_FOUND"
            del self.store[key]
            return "OK"

        return "BAD_COMMAND"

    def CheckCommand(self, command):
        operator, key, value = command.split()
        if operator == "SET":
            return "OK"
        if operator == "GET":
            return "OK" if key in self.store else "NOT_FOUND"
        if operator == "DEL":
            return "OK" if key in self.store else "NOT_FOUND"

        return "BAD_COMMAND"
