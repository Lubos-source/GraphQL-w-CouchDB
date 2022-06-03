import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

from randomdater import GroupTypeDataFun, RoleDataFun, GroupDataFun

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
	name=TextField()
	surname=TextField()
	address=TextField()
	email=TextField()
	publish_date=DateTimeField(default=datetime.now())


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

#################################################
## vytvoreni databaze							#
db=create_database('funkcetest',0)				#
#################################################


"""
def insert_random_data():
	result= db.testovaci_databaze.insert_many(
		[getFullRndDoc() for i in range(6)]
	)
"""

def print_all(type):
	vysledek={}
	n=1
	for dokumenty in db:
		doc=db[dokumenty]
		vys={}
		skupiny={}
		if(doc["type"]==type):
			vys=find_first(doc["_id"])
			"""for row in doc:
				if (str(row)=="groups"):
					vys["groups"]=[]
					for group in doc["groups"]:
						skupiny[group]=find_first(group)
					for key in skupiny:
						vys["groups"].append(skupiny[key])
				else:
					vys[str(row)] = (doc[row])"""
			vysledek['data'+str(n)]=vys #zkouska dictionary v dictionary
			n=n+1
	return vysledek

def insert_document(dokum):
	#documentid=docID
	document=dokum
	ajdi=document['_id']
	if ajdi in db:
		#print("\nDokument s ID '"+ajdi+"' jiz existuje v databazi '"+ str(db)+"'")
		r=find_first(ajdi)
		result=r.copy()
		result.update({'_id': ajdi +"  + info : (Prvek jiz existuje v databazi)"})
	else:
		#print("\nVkladam dokument '"+ ajdi +"' do databaze '"+ str(db)+"'")
		document['publish_date']=str(datetime.now())
		db.save(document)
		ajdi=document['_id']
		result= find_first(ajdi)

		#db["Group-all-users"]
		#if (dokum["type"]!="group"):
		#	update_group_members("Group-all-users",ajdi)

	return result

def insert_pymodel(ttl="testdefault"):
	#person=UserDataInput(_id="id#"+str(datetime.now())+"#id",name=ttl, surname="42", address="adresa 15/666", email= ttl+"email@default.com")
	#person.store(db)
	return 0
	
def update_user(updateDoc,docid):
	####UPDATE DOCUMENT####	#komentare zatim nechavam, kdyby me napadl jiny zpusob pomoci nacteni(load), zemny a ulozeni (store)... ale zatim takhle :)
	if(db[docid]["type"]=="user"):

		puvodni={}
		doc=db[docid]
		for row in doc:
				puvodni[str(row)] = (doc[row])
		#print("Puvodni dict: ", puvodni)
		vysledek=puvodni.copy()
		vysledek.update(updateDoc)
		db.save(vysledek)										#nevyhoda muze ulozit i neco navic.... pokud vlozi nejaky dalsi klic do update dictionary....
		updater = UserDataInput.load(db, docid)
		#print("Data Po UPDATE: ", updater)
	return 1

def update_user_group(docid, groupID, grproleID):
	#print("user ", db[docid]['_id'], " group ", db[groupID]['_id'], "grprole: ", grproleID)
	if (((db[docid]['_id'] in db) and (db[docid]["type"]=="user")) and ((db[groupID]['_id'] in db) and (db[groupID]["type"]=="group"))and(db[grproleID]['_id'] in db)):
		puvodni={}
		grpuvodni=[]
		doc=db[docid]
		for row in doc:
			puvodni[str(row)] = doc[row]
		vysledek=puvodni.copy()

		for grup in vysledek["groups"]:
			#print("Group ID: ", grup)
			grpuvodni.append(grup["grpid"])
			#print("Group puvodni ID: ", grpuvodni["_id"])
		#grpuvodni.append(groupID)
		vysledek["groups"].append({"grpid":groupID, "grprole":grproleID}) if groupID not in grpuvodni else vysledek["groups"]
		#print("debug 1 ")
		#vysledek["groups"].append(grpuvodni) if grpuvodni["_id"] not in grupy else vysledek["groups"]
		db.save(vysledek)
		#print("debug 2 ")
		update_group_members(groupID, docid)
		#print("debug 3 ")
	return(find_first(docid))


def update_group_members(groupID, userID):
	#print("\n---------------provadim funkci UPDATE GROUP!!!--------\n")
	if ((db[userID]['_id'] in db) and (db[groupID]['_id'] in db)):
		puvodni={}
		membpuvodni=[]
		doc=db[groupID]
		for row in doc:
			puvodni[str(row)] = doc[row]
		vysledek=puvodni.copy()
		for mem in vysledek["members"]:
			membpuvodni.append(mem)
		vysledek["members"].append(userID) if userID not in membpuvodni else vysledek["members"]
		#vysledek["members"].append(memb) if memb["_id"] not in membersarray else vysledek["members"]
		db.save(vysledek)
		

	#return 0

def del_documents():
	#print("\nodstranuji veskere dokumenty v databazi '"+str(db)+"' ...")
	
	for dok in db:
		#dint=int(dok)
		#db.delete(dint)
		del db[dok]
		#print("'"+dok + "' uspesne odstranen !")

def del_doc(docid):
	vysledek={}
	if ((docid in db)and(db[docid]["type"]=="user")):
		doc=db[docid]
		newlistgrp=db[docid]["groups"]
		#print("list vsech skupin: ", newlistgrp)
		for grp in newlistgrp:
			newlistmembers=db[grp["grpid"]]["members"]
			newlistmembers.remove(docid)
			#print("po list: ", newlistmembers)
			novy=db[grp["grpid"]]
			novy["members"]=newlistmembers
			#print("ukladam : ", str(novy))
			db.save(novy)
		#print("PO remove list + UPDATE : ", db[skupina]["members"])
		db.delete(doc)

	elif((docid in db)and(db[docid]["type"]=="group")): #Mozna dodelat podminku aby nemohl odstranit def skupinu pro vsechny users (Group-all-users) ?
		for member in db[docid]["members"]:
			newlistgrps=db[member]["groups"]
			#print("pred remove list: ", newlistgrps)
			for i in range(len(newlistgrps)):
				if (newlistgrps[i]['grpid'] == docid):
					del newlistgrps[i]
					break
			#newlistgrps.remove(docid)
			#print("---Po remove list: ", newlistgrps)
			novy=db[member]
			novy["groups"]=newlistgrps
			db.save(novy)
			#print("PO remove list + UPDATE : ", db[member]["groups"])
		db.delete(db[docid])

	else:
		return({"name":"DELETE-exception", "message":"Documents doesnt exist in DBS check your argument and his type (user/group)"})
	vysledek['name']="sucessfull-DELETE"
	vysledek['message']="succesfully deleted document from dbs"
	return(vysledek)

def find_first(docname):
	vysledek={}
	for dokumenty in db:
		if dokumenty==docname:
			#print("DEBUG1 ---dokument nalezen v dbs---")
			doc=db[dokumenty]
			skupiny={}
			members={}
			for row in doc:
				#print("DEBUG2 ---row in Pozadovany dokument---", "row:   ", str(row))
				if (str(row)=="groups"):
					#print("DEBUG3---row is GROUPS---", "row:   ", str(row))
					vysledek["groups"]=[]
					for group in doc["groups"]:
						#print("DEBUG4---for row is GROUPS---", "grup:   ", str(group))
						grpvys={}
						#print("DEBUG4.1---pristup k prvku v dict groups---", "prvek_:   ", str(group["grpid"]))
						grpdoc=db[group["grpid"]]
						#print("DEBUG5---document dane Group---", "grpdoc:   ", str(grpdoc))
						for row in grpdoc:
							#print("DEBUG6 ---for row in grpdoc---", "row:   ", str(row))
							if(str(row)=="members"):
								#print("DEBUG7 ---row == members---", "row:   ", str(row))
								grpvys["members"]=grpdoc[row]
								#print("ukladam tam : ", str(grpdoc[row]))
								#print("DEBUG7.1 ---grpvys[members]:---", "obsah:   ", str(grpvys["members"]))
								grpidslist=[]
								for member in grpvys["members"]:
									#print("DEBUG8 ---for member in docMMEBERS---", "row:   ", str(grpvys["members"]))
									grpvysdoc=db[member]
									#print("user: mebers ",grpvysdoc)
									grpvysdoc["groups"]=[{"_id":"Moc Dlouhy Retezec"}] #Varovna hlaska ktera se ukaze v ID pokud bude uzivatel moc retezit ---> prozatimni zamezeni NEKONECNEMU cyklu !!
									grpidslist.append(grpvysdoc)
								grpvys["members"]=grpidslist
								#print("DEBUG9 ---grpvys[members]:---", "obsah:   ", str(grpvys["members"]))
							elif(str(row)=="groupType"):
								#print("DEBUG10 ---row == groupType :---", "obsah:   ", str(row))
								grpvys["groupType"]=grpdoc[row]
								#print("DEBUG11 --- grpvys[groupType] :---", "obsah:   ", str(grpdoc[row]))
								grpidslist=[]
								for typ in grpvys["groupType"]:
									#print("DEBUG12 --- typ v grpvys[grouptype] :---", "obsah:   ", str(typ))
									grpvysdoc=db[typ]
									#print("DEBUG13 --- hledej typ v dbs :---", "obsah:   ", str(grpvysdoc))
									grpidslist.append(grpvysdoc)
								grpvys["groupType"]=grpidslist
								#print("DEBUG14 --- vyledny grpvys[grouptype] v dbs :---", "obsah:   ", str(grpvys["groupType"]))
								### DEBUG final result: srpávně uloží vše co chceme ! Bud chyba jinde nebo potrebujeme \
								# misto typu <DOC ....> jen {} ---> cyklus. 
							else:
								grpvys[str(row)]=grpdoc[row]
								#print("DEBUG15 --- vyledny grpvys[row] v dbs :---", "obsah:   ", str(grpvys[str(row)]))
						#print("DEBUG16 --- vysledny vysledek ktery se ulozi do documentu v dbs :---", "obsah:   ", str(grpvys))
						grptypes=[]
						for prvky in grpvys["groupType"]:
							grouptype={}
							#print("DEBUG16.1 --- prvky v grpType :---", "obsah:   ", str(prvky), " IN_:",str(grpvys["groupType"]))
							for row in prvky:
								#print("DEBUG16.1.1 --- row v prvky :---", "obsah:   ", str(row), " IN_:",str(prvky))
								grouptype[str(row)]=prvky[str(row)]
						grptypes.append(grouptype)
						#print("DEBUG16.2 --- vse v grpTypes :---", "obsah:   ", str(grptypes))
						#print("DEBUG16.2.1 --- skupiny :---", "obsah:   ", str(skupiny), " group: ", str(group["grpid"]))
						grpid=group["grpid"]
						skupiny[grpid]=grpvys
						skupiny[grpid]["groupType"]=[]
						#print("DEBUG16.3 --- prazdne grptype in skupiny :---", "obsah:   ", str(skupiny[grpid]))
						skupiny[grpid]["groupType"]=grptypes
						#print("DEBUG16.3 --- NAPLNENO grptype in skupiny :---", "obsah:   ", str(skupiny[grpid]))
						#print("DEBUG17 --- vysledny skupiny :---", "obsah:   ", str(skupiny))

					for key in skupiny:

						vysledek["groups"].append(skupiny[key])

				elif((str(row)=="members")and(doc["type"]=="group")):
					memberlist=[]
					memvys={}
					for member in doc["members"]:
						#print("debug member in members:", " v : ",doc["members"], " je: ",member)
						memvysdoc={}
						for memrow in db[member]:
							memvysdoc[str(memrow)]=db[member][memrow]
						#memvysdoc=db[member]
						#print("grp vys: ", memvysdoc)
						memvysdoc["groups"]=[{"_id":"Moc Dlouhy Retezec --> Pro zobrazeni pozadovanych hodnot zvolte novy prikaz v GQL !!!"}] #Varovna hlaska ktera se ukaze v ID pokud bude uzivatel moc retezit ---> prozatimni zamezeni NEKONECNEMU cyklu !!
						#print("grp vys pop nul group: ", memvysdoc)
						memberlist.append(memvysdoc)
						#print("grpLIST vys: ", memberlist)
					memvys["members"]=memberlist
					vysledek["members"]=memberlist
				
				elif((str(row)=="groupType")and(doc["type"]=="group")):
					grptypelist=[]
					grptypevys={}
					for grptype in doc["groupType"]:
						typevys={}
						for row in db[grptype]:
							typevys[str(row)]=db[grptype][str(row)]
						grptypelist.append(typevys)
					vysledek["groupType"]=grptypelist
				else:
					vysledek[str(row)]=(doc[row])	#POKUD bude chyba tak zde bylo : vysledek[str(row)]=str(doc[row])	KDYSI jsem upravil prave kvuli chybe, ted zatim v pohode + vyresi problemy s groups
			#print("vysledek obsahuje:",vysledek)
			return vysledek
	return vysledek



#-------program-databaze-testing--------#


dataGRPtype=GroupTypeDataFun()
dataRoletype=RoleDataFun()
dataGroup=GroupDataFun()

print(".............vkladam data do databaze.............")
for data in dataGRPtype:
	insert_document(data)
print("group type data vlozena! ")

for data in dataRoletype:
	insert_document(data)
print("role type data vlozena! ")

for data in dataGroup:
	insert_document(data)
print("Def Group ulozeny do dbs")


#db=create_database('funkcetest', 0) #('nazevdatabaze', 1-zapnuti komentare)
#insert_pymodel("Johny")
#insert_pymodel("test")
#insert_pymodel()
#insert_pymodel('funkcetest')
#insert_document(db,'dokumentID')

#update_user(db,"updatedoc")

#zkouska=print_all()

#print("Zkouska DICTIONARY:\n", zkouska) #funguje 

#find_first("faffe2acc80cce5bf5d747dda1004dd1")

#del_documents(db)


####TODO:
#get user by email ?
#get users by name ? (list of users with same name)
#relation between user and group and group type (zkusit jen ID do listu a při query použit funkci find(ID), kter doplní obejkt podle uloženého ID 
#PRINT ALL upravit aby query precetlo list IDs a vratilo jejich objekt ! 01.06.2022

