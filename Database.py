class Database:
    def __init__(self):
        self.store = {}
    
    def ApplyCommand(self, command):
        operator, key, value = command.split()
        if operator == "SET":
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
