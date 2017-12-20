# app.py
import os

import falcon
import pika

from controllers import NoteResourceController
from db_client import *

__author__ = "Naren_Aryan, @wolfhesse"
__written_date__ = "13-09-2015:Saturday"
__modification_date = '2017-11-29'
__title__ = "Falcon and PyPy for building massively scalable RESTFul API"

RDB_HOST = os.environ.get('RDB_HOST') or '10.0.0.100'
RDB_PORT = os.environ.get('RDB_PORT') or 28015

PROJECT_DB = 'sms'
PROJECT_TABLE = 'webhooks'

config = {'host': RDB_HOST, 'port': RDB_PORT, 'db': PROJECT_DB, 'table': PROJECT_TABLE}
db_connection = connectAndSetup(config)

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(
    pika.ConnectionParameters('s0.wolfslab.wolfspool.at', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='hello', durable=True)
channel.close()
connection.close()


api = falcon.API()
api.add_route('/notes/{system}', NoteResourceController(db_connection, PROJECT_DB, PROJECT_TABLE, channel))
api.add_route('/notes', NoteResourceController(db_connection, PROJECT_DB, PROJECT_TABLE, channel))

# at end: channel.close()
