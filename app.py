# app.py

__author__ = "Naren_Aryan"
__written_date__ = "13-09-2015:Saturday"
__title__ = "Falcon and PyPy for building massively scalable RESTFul API"

import json

import falcon

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

    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            print '1'
            raw_json = req.stream.read()
            print raw_json
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Error',
                ex.message)
 
        try:
            result = json.loads(raw_json, encoding='utf-8')
            data = {'pstate': 'initial', 'type': 'falcon-order-webhook-rcv', 'request': 'post', 'system': 'rcs2',
                    'order': result}

            #sid = r.db(PROJECT_DB).table(PROJECT_TABLE).insert({'title':'webhook', 'data':result}).run(db_connection)
            sid = r.db(PROJECT_DB).table(PROJECT_TABLE).insert(data).run(db_connection)
            #sid = r.db(PROJECT_DB).table(PROJECT_TABLE).insert({'title':result['title'],'body':result['body']}).run(db_connection)
            #resp.body = 'Successfully inserted %s'%sid
            resp.body = '%s'%json.dumps(sid)
            print '2'
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Invalid JSON',
                'Could not decode the request body. The '
                'JSON was incorrect.')

        def on_delete(self, req, resp):
            """Handles GET requests"""
            # Return all notes
            note_cursor = r.db(PROJECT_DB).table(PROJECT_TABLE).run(db_connection)
            notes = [i for i in note_cursor]
            resp.body = json.dumps({'notes':notes})

api = falcon.API()
api.add_route('/notes', NoteResource())
