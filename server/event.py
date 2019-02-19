from datetime import datetime

class Event():

    def __init__(self, id, sensor_id, timestamp, message):
        self.id = id
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.message = message

    def to_string(self):
        return '{:<50} {:<18} {:<10}'.format(str(self.timestamp) + ': ', 'Sensor ID #' + str(self.sensor_id), '- ' + self.message)
