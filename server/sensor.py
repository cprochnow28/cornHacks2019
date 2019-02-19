class Sensor():

    def __init__(self, id, type, secret):
        self.id = id
        self.type = type
        self.secret = secret
        self.online = False
        self.name = self.to_string()

    def to_string(self):
        return '{:<27}{:<10}'.format('> Sensor ID #' + str(self.id) + ': ' + self.type, ' ')
