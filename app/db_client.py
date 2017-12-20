
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError


def createConnection(host, port):
    connection = r.connect(host, port)
    return connection


# This is just for cross-checking database and table exists
def setupDbAndTable(connection, db, table):
    print(db, connection)
    try:
        r.db_create(db).run(connection)
        print('Database setup completed.')
    except RqlRuntimeError:
        try:
            r.db(db).table_create(table).run(connection)
            print('Table creation completed')
        except:
            print('Table already exists.Nothing to do')


def connectAndSetup(options):
    host = options['host']
    port = options['port']
    db = options['db']
    table = options['table']
    connection = createConnection(host, port)
    setupDbAndTable(connection, db, table)
    return connection
