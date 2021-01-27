

class JSONSchema:
    def __init__(self):
        self.links = {}
        self.data = {}

    def json(self):
        return self.__dict__
