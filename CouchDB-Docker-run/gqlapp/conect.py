
from email.policy import default
import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

from graphqlaplication import getFullRndDoc

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
    couchserver = couchdb.Server(url='http://admin:admin@couch:5984/')
    couchserver.resource.credentials = ("admin", "admin")

    return couchserver

###mapování dokumentu do python objektu:

class UserDataInput(Document):
	_id= TextField()
	title=TextField()
	instructor=IntegerField()
	publish_date=DateTimeField(default=datetime.now)


class UserDataShow(Document):
	_id= TextField()
	title=TextField()
	instructor=IntegerField()
	publish_date=DateTimeField()


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


# vytvoreni databaze
db=create_database('testovaci_databaze',0)

def insert_random_data():
	result= db.testovaci_databaze.insert_many(
		[getFullRndDoc() for i in range(6)]
	)

def print_all():
	print("\nVypis vsech dokumentu v : "+ str(db))
	vysledek=list()
	for dokumenty in db:
		print("\ndokument ID: " + dokumenty)
		vysledek.append('id')
		vysledek.append(dokumenty)
		doc=db[dokumenty]
		print("V dokumentu (ID: '"+dokumenty+"') se nachazi:")
		for row in doc:
			print("--radek: \""+str(row) +"\" --obsah: \""+str(doc[row])+"\"")
			vysledek.append(str(row))
			vysledek.append(str(doc[row]))
	return vysledek

def insert_document(dokum, docID):
	documentid=docID
	document=dokum
	if documentid in db:
		print("\nDokument s ID '"+documentid+"' jiz existuje v databazi '"+ str(db)+"'")
		doc_id=documentid
	else:
		print("\nVkladam dokument '"+ documentid +"' do databaze '"+ str(db)+"'")
		#db.save({'_id':documentid, document})
		result= db.testovaci_databaze.insert_one(document)
		return result

def insert_pymodel(ttl="testdefault"):
	person=UserDataInput(_id="id#"+str(datetime.now())+"#id",title=ttl, instructor="42")
	person.store(db)

def update_user(newjmeno,docid):
	####UPDATE DOCUMENT####
	person = UserDataInput.load(db, docid)
	person.name = newjmeno
	person.store(db)
	#print(person.name)

def del_documents():
	print("\nodstranuji veskere dokumenty v databazi '"+str(db)+"' ...")
	
	for dok in db:
		#dint=int(dok)
		#db.delete(dint)
		del db[dok]
		print("'"+dok + "' uspesne odstranen !")



def find_first(docname):
	for dokumenty in db:
		if dokumenty==docname:
			doc=db[dokumenty]
			print("\nV dokumentu (ID: '"+dokumenty+"') se nachazi:")
			for row in doc:
				print("--radek: \""+str(row) +"\" --obsah: \""+str(doc[row])+"\"")
			break


#-------program-databaze-testing--------#


db=create_database('funkcetest', 1) #('nazevdatabaze', 1-zapnuti komentare)
insert_pymodel("Johny")
insert_pymodel("test")
insert_pymodel()
#insert_pymodel('funkcetest')
#insert_document(db,'dokumentID')

#update_user(db,"updatedoc")

print_all()


#find_first(db,"faffe2acc80cce5bf5d747dda1004dd1")

#del_documents(db)
