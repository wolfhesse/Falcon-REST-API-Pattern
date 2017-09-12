# app.py

__author__ = "Naren_Aryan"
__written_date__ = "13-09-2015:Saturday"
__title__ = "Falcon and PyPy for building massively scalable RESTFul API"

import json

import falcon
import pika

from db_client import *


class NoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        # Return note for particular ID
        if req.get_param("id"):
            result = {'note': r.db(PROJECT_DB).table(PROJECT_TABLE).get(req.get_param("id")).run(db_connection)}
        else:
            note_cursor = r.db(PROJECT_DB).table(PROJECT_TABLE).run(db_connection)
            result = {'notes': [i for i in note_cursor]}
        print result
        resp.body = json.dumps(result)

    def on_post(self, req, resp, system):

        finished = False

        if not finished:

            try:
                raw_json = req.stream.read()
                print raw_json
            except Exception as ex:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       'Error',
                                       ex.message)

            if raw_json.startswith('webhook_id'):
                resp.body = 'step0'
                print 'webhook'
                finished = True

        if not finished:
            resp.body = 'step1'

            try:
                result = json.loads(raw_json, encoding='utf-8')

                data = {'pstate': 'initial',
                        'type': 'falcon-webhook-rcv',
                        'request': 'post',
                        # 'payload': result,
                        # 'headers': req.headers,
                        'detail': {
                            'headers': req.headers,
                            'sent': result
                        },
                        'system': system}
                # data['detail'] = {}
                # data['detail']['headers'] = req.headers
                # data['detail']['sent'] = result

                # sid = r.db(PROJECT_DB).table(PROJECT_TABLE).insert({'title':'webhook', 'data':result}).run(db_connection)
                sid = r.db(PROJECT_DB).table(PROJECT_TABLE).insert(data).run(db_connection)
                # sid = r.db(PROJECT_DB).table(PROJECT_TABLE).insert({'title':result['title'],'body':result['body']}).run(db_connection)
                # resp.body = 'Successfully inserted %s'%sid
                resp.body = '%s' % json.dumps(sid)
                print 'step1'
            except ValueError:
                raise falcon.HTTPError(falcon.HTTP_400,
                                       'Invalid JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect.')

            resp.body = "step2"

            credentials = pika.PlainCredentials('test', 'test')
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('s0.wolfslab.wolfspool.at', credentials=credentials))
            channel = connection.channel()
            channel.queue_declare(queue='hello', durable=True)

            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body="%s" % json.dumps(data))
            channel.close()
            print 'step3'

        resp.body = '{"webhook-note":"OK"}'

    def on_delete(self, req, resp):
        """Handles GET requests"""
        # Return all notes
        note_cursor = r.db(PROJECT_DB).table(PROJECT_TABLE).run(db_connection)
        notes = [i for i in note_cursor]
        resp.body = json.dumps({'notes': notes})


api = falcon.API()
api.add_route('/notes/{system}', NoteResource())
