import datetime
import json

import falcon
import pika
import rethinkdb as r

from db_client import setupDbAndTable


class NoteResourceController:
    def __init__(self, connection, db, table, channel):
        self.connection = connection
        self.db = db
        self.table = table
        self.channel = channel

    def on_get(self, req, resp):
        """Handles GET requests"""
        # Return note for particular ID
        if req.get_param("id"):
            result = {'note': r.db(self.db).table(self.table).get(req.get_param("id")).run(self.connection)}
            print("response for get:notes, id request: " + req.get_param("id"))
        else:
            note_cursor = r.db(self.db).table(self.table).run(self.connection)
            result = {'notes': [i for i in note_cursor]}
            print("response for get:notes, all")
        # print(result)
        resp.body = json.dumps(result)

    def on_post(self, req, resp, system):

        finished = False
        data = {}
        resp.body = ""

        if not finished:
            print('step0')
            try:
                raw_post_bytes = req.stream.read()
                print(raw_post_bytes)
            except Exception as ex:
                print('step0 exception')
                raise falcon.HTTPError(falcon.HTTP_400,
                                       'Error',
                                       ex.message)

            raw_post = raw_post_bytes.decode('utf-8')

            print('step1')
            if raw_post.startswith(('webhook_id', 'test')):
                json.dumps({"webhook-note": "CREATED", "data": raw_post})
                resp.body = 'webhook detected'
                print('step1 ok: webhook or test')
                finished = True

        if not finished:

            now = datetime.datetime.now()
            d = now.date()
            t = now.time()

            print("step2 at {0}, {1}".format(d, t))
            try:
                # post_data = json.loads(raw_post, encoding='utf-8')
                post_data = json.loads(raw_post)

                data = {
                    'processing_state': 'initial',
                    'ts': str(datetime.datetime.now()),
                    'type': 'falcon-webhook-rcv',
                    'request': 'post',
                    # 'payload': post_data,
                    # 'headers': req.headers,
                    'post_data': {
                        'headers': req.headers,
                        req.headers['X-WC-WEBHOOK-RESOURCE']: post_data,
                    },
                    'system': system,
                }

                # store in system - specific table
                setupDbAndTable(self.connection, self.db, system)
                insert_result = r.db(self.db).table(system).insert(data).run(self.connection)
                print(insert_result)

                # store in sms table (catalog)
                data['rt_system_id'] = insert_result['generated_keys'][0]
                insert_result = r.db(self.db).table(self.table).insert(data).run(self.connection)
                print(insert_result)

                data['rt_webhooks_id'] = insert_result['generated_keys'][0]
                resp.body = json.dumps({"status": 'OK', 'id': insert_result['generated_keys'][0]})

            except ValueError:
                print('step2 exception')
                raise falcon.HTTPError(falcon.HTTP_400,
                                       'Invalid JSON',
                                       'Could not decode the request body. The '
                                       'JSON was incorrect.')

            print('step3')
            try:
                credentials = pika.PlainCredentials('test', 'test')
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters('s0.wolfslab.wolfspool.at', credentials=credentials))
                channel = connection.channel()
                channel.queue_declare(queue='hello', durable=True)

                channel.basic_publish(exchange='',
                                      routing_key='hello',
                                      body="%s" % json.dumps(data))
                channel.close()
                connection.close()
            except:
                print('step3 exception')

            print('ok')
            # def on_delete(self, req, resp):
            #     """Handles GET requests"""
            #     # Return all notes
            #     note_cursor = r.db(PROJECT_DB).table(PROJECT_TABLE).run(db_connection)
            #     notes = [i for i in note_cursor]
            #     resp.body = json.dumps({'notes': notes})
