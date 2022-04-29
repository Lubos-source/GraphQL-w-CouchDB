
import couchdb

###---------Connection:------------------------###
"""
definovani funkci pro praci s databazi
-connection string ke couchdb serveru + credentials
-vytvoreni databaze na couchdb serveru
-vypsani dokumentu v dane databazi + radky a obsah
-vlozeni dokumentu s vlastnim ID
-vlozeni dokumentu pomoci definovane tridy UserDataInput()
-update usera v databazi a dokumnetu s ID v parametru
-odstraneni vsech dokumentu v databazi
-nalezeni dokumentu s ID (parametr) v databazi (parametr)
"""


def conectToCouch():
    couchserver = couchdb.Server(url='http://root:example@127.0.0.1:31005/')
    couchserver.resource.credentials = ("root", "example")

    return couchserver

###mapování dokumentu do python objektu:

from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

class UserDataInput(Document):
	name=TextField()
	age=IntegerField()
	added=DateTimeField(default=datetime.now)


class UserDataShow(Document):
	name=TextField()
	age=IntegerField()
	added=DateTimeField()


######---tvorba-funkcipro-komunikaci-s-databazi---#########

def create_database(dbname,n=0):
	dbname=dbname
	databaze=conectToCouch()

	if dbname in databaze:
		if n==1:
			print("Databaze '"+dbname+ "' se zde uz nachazi.\n")
			databaze[dbname]
	else:
		if n==1:
			print("Databaze '" +dbname+"' neexistuje a bude vytvorena.\n");
		databaze.create(dbname)

	return databaze[dbname]

def print_all(dbarg):
	print("\nVypis vsech dokumentu v : "+ str(dbarg))
	db=dbarg
	for dokumenty in db:
		print("\ndokument ID: " + dokumenty)
		doc=db[dokumenty]
		print("V dokumentu (ID: '"+dokumenty+"') se nachazi:")
		for row in doc:
			print("--radek: \""+str(row) +"\" --obsah: \""+str(doc[row])+"\"") 

def insert_document(dbarg, docID):
	documentid=docID
	db=dbarg
	if documentid in db:
		print("\nDokument s ID '"+documentid+"' jiz existuje v databazi '"+ str(db)+"'")
		doc_id=documentid
	else:
		print("\nVkladam dokument '"+ documentid +"' do databaze '"+ str(db)+"'")
		db.save({'_id':documentid,'type': 'Manualni', 'name': 'BezPYmodelu-vlastni-ID'})

def insert_pymodel(dbname):
	db=create_database(dbname)
	person=UserDataInput(name="Johnny Deep", age="42")
	person.store(db)

def update_user(dbarg,docid):
	####UPDATE DOCUMENT####
	db=dbarg
	person = UserDataInput.load(db, docid)
	person.name = 'Zmena Jmena :)'
	person.store(db)
	#print(person.name)

def del_documents(dbarg):
	db=dbarg
	print("\nodstranuji veskere dokumenty v databazi '"+str(db)+"' ...")
	
	for dok in db:
		#dint=int(dok)
		#db.delete(dint)
		del db[dok]
		print("'"+dok + "' uspesne odstranen !")



def find_first(dbarg,docname):
	for dokumenty in dbarg:
		if dokumenty==docname:
			doc=dbarg[dokumenty]
			print("\nV dokumentu (ID: '"+dokumenty+"') se nachazi:")
			for row in doc:
				print("--radek: \""+str(row) +"\" --obsah: \""+str(doc[row])+"\"")
			break


#-------program-databaze-testing--------#


db=create_database('funkcetest', 1) #('nazevdatabaze', 1-zapnuti komentare)

#insert_pymodel('funkcetest')
#insert_document(db,'dokumentID')

#update_user(db,"updatedoc")

print_all(db)

#find_first(db,"faffe2acc80cce5bf5d747dda1004dd1")

#del_documents(db)
