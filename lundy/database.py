import os
import urllib

from mongomock import MongoClient


def get_database():
    config_path = os.environ.get('LUNNICONFIG')
    if not config_path:
        raise "MISS CONFIGURATION"
    with open(config_path) as f:
        for line in f:
            command = line[:-1]
            command = command.split('=')
            if command[0] == 'uri':
                uri_path = command[1]
    uri_path = urllib.quote_plus(uri_path)
    client = MongoClient(uri_path)
    db = client.lunni_test
    return db