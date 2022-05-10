import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

from randomdater import getFullRndDoc

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
	publish_date=DateTimeField(default=datetime.now())


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
db=create_database('funkcetest',0)

def insert_random_data():
	result= db.testovaci_databaze.insert_many(
		[getFullRndDoc() for i in range(6)]
	)

def print_all():
	print("\nVypis vsech dokumentu v : "+ str(db))
	#vysledek=list()
	vysledek={}
	n=1
	for dokumenty in db:
		#print("\ndokument ID: " + dokumenty)
		doc=db[dokumenty]
		print("V dokumentu (ID: '"+dokumenty+"') se nachazi: ")
		vys={}
		for row in doc:
			#vysledek[str(row)]=str(doc[row])
			print("--radek: \""+str(row) +"\" --obsah: \""+str(doc[row])+"\"")
			vys[str(row)] = str(doc[row])
		vysledek['data'+str(n)]=vys #zkouska dictionary v dictionary
		#vysledek.append(vys)
		n=n+1
	return vysledek

def insert_document(dokum):
	#documentid=docID
	document=dokum
	ajdi=document['_id']
	if ajdi in db:
		print("\nDokument s ID '"+ajdi+"' jiz existuje v databazi '"+ str(db)+"'")
		r=find_first(ajdi)
		result=r.copy()
		result.update({'_id': ajdi +"  + info : (Prvek jiz existuje v databazi)"})
	else:
		print("\nVkladam dokument '"+ ajdi +"' do databaze '"+ str(db)+"'")
		document['publish_date']=str(datetime.now())
		db.save(document)
		ajdi=document['_id']
		result= find_first(ajdi)
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
	vysledek={}
	for dokumenty in db:
		if dokumenty==docname:
			doc=db[dokumenty]
			print("\nV dokumentu (ID: '"+dokumenty+"') se nachazi:")
			for row in doc:
				print("--radek: \""+str(row) +"\" --obsah: \""+str(doc[row])+"\"")
				vysledek[str(row)]=str(doc[row])
			return vysledek


#-------program-databaze-testing--------#


db=create_database('funkcetest', 0) #('nazevdatabaze', 1-zapnuti komentare)
#insert_pymodel("Johny")
#insert_pymodel("test")
#insert_pymodel()
#insert_pymodel('funkcetest')
#insert_document(db,'dokumentID')

#update_user(db,"updatedoc")

zkouska=print_all()

print("Zkouska DICTIONARY:\n", zkouska) #funguje 

#find_first("faffe2acc80cce5bf5d747dda1004dd1")

#del_documents(db)
