#pip install couchdb

import couchdb

###---------Connection:------------------------###

couchserver = couchdb.Server(url='http://admin:admin@127.0.0.1:31111/')
couchserver.resource.credentials = ("admin", "admin")

###-------Test vypisu databaze z couchdb:------###

#db = couchserver['testdata']
print("\nvsechny databaze:")
for dbname in couchserver:
    print(dbname)

###Create:

dbname = "testingdata"

if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

print("\nDatabaze po create:")
for dbname in couchserver:
    print(dbname)

###Delete:
dbname = "mydb"

if dbname in couchserver:
    del couchserver[dbname]
else:
    print("Databaze neexistuje")

print("\nDatabaze po delete:")
for dbname in couchserver:
    print(dbname)
