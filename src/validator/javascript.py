from src.request.connection import Connection
import json


class Javascript(object):
    HOSTNAME = 'https://phantomvalidator.javabudd.com'
    CONDITION_ALERT = 'alert'

    def __init__(self):
        self.connection = Connection()

    def validate(self, response, condition):
        validated = False

        response = self.connection.request(
            self.HOSTNAME,
            json.dumps({
                'response': response,
                'condition': condition
            }),
            {}
        )

        if response is not None:
            validated = True

        return validated
