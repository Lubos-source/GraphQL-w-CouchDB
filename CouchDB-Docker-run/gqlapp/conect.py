#from sqlite3 import connect
import couchdb

###---------Connection:------------------------###



def conectToCouch():
    couchserver = couchdb.Server(url='http://admin:admin@127.0.0.1:31111/')
    couchserver.resource.credentials = ("admin", "admin")

    return couchserver

