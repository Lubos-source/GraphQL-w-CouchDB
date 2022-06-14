import random
import couchdb

from datetime import datetime


from randomdater import PersonDataFun, RoleDataFun, GroupDataFun, GroupTypesDataFun, Relations

###---------Connection:------------------------###

DB_Name_To_Create="prekopavka"

def conectToCouch():
    couchserver = couchdb.Server(url='http://admin:admin@couch:5984/')
    couchserver.resource.credentials = ("admin", "admin")

    return couchserver

######---tvorba-funkcipro-komunikaci-s-databazi---#########
def create_database(dbname,debug=0):
	dbname=dbname
	databaze=conectToCouch()

	if dbname in databaze:
		if debug==1:
			print("Databaze '"+dbname+ "' se zde uz nachazi.\n")
			databaze[dbname]
	else:
		if debug==1:
			print("Databaze '" +dbname+"' neexistuje a bude vytvorena.\n")
		databaze.create(dbname)

	return databaze[dbname]

def connectToDatabase(dbname):
	databaze=conectToCouch()
	if dbname in databaze:
		return(databaze[dbname])
	else:
		return({"message":"Database doesnt exist, please use create_database(DB_Name) FIRST!"})
#################################################
## vytvoreni databaze							#
db=create_database(DB_Name_To_Create,0)			#
#################################################


def insert_document(dokument_data):
	doc=dokument_data
	if doc['_id'] in db:
		r=find_first(doc['_id'])
		result=r.copy()
		#print("result : ", result)
		result.update({'_id': doc['_id'] +"  + info : (Prvek jiz existuje v databazi)"})
		#print("EXISTUJE, takze result po update: ", result)
	else:
		#doc['publish_date']=str(datetime.now())
		db.save(doc)
		result= find_first(doc['_id'])
	return result

def del_doc(doc):
	db.delete(doc)

def find_first(docid):	
	vysledek=db.get(docid)
	return vysledek

#===============================================================================#

class Group:
    def __init__(self, name = None, groupType = None):
        self.id = None 
        self.name = name
        self.groupType = groupType

    def Load(self, grpID):
        self.id=grpID
        grp=find_first(grpID)
        grp=grp.copy()
        self.name=grp["name"]
        self.groupType=grp["groupType"]

    def GetGroupType(self):
        grt=GroupType()
        grt.Load(self.groupType)
        return(grt)

    def LoadMembers(self):
        grpid=self.id
        vys=[]
        for doc in db:
            try:
                if((db[doc]["type"]=="relation") & (db[doc]["groups_id"]==grpid)):
                    prvek=find_first(db[doc]["_id"])
                    prvek=prvek.copy()
                    vys.append(prvek["users_id"])
                else:
                    pass
            except:
                pass
        return(vys)

    def GetMembers(self):
        memberlistofIDs=self.LoadMembers()
        out=[]

        for id in memberlistofIDs:
            prsn=Person()
            prsn.Load(id)
            out.append(prsn)
        return(out)

    def AddtoDB(self):
        data={
            "_id":None,
            "id":None,
            "name":str(self.name),
            "groupType":str(self.groupType)
        }
        self.id="idGrp-"+str(random.randrange(999999999999))+str(datetime.timestamp(datetime.now())).replace(".","T")+str(random.randrange(999999999999))
        data["_id"]=self.id
        data["id"]=data["_id"]
        insert_document(data)

    def AddMember(self, member_id, roleType_id):
        grpID=self.id
        exist=0
        existedidofRelat=""
        if((grpID in db)&(member_id in db)&(roleType_id in db)):
            for doc in db:
                try:
                    if((db[doc]["type"]=="relation")&(db[doc]["groups_id"]==grpID)&(db[doc]["users_id"]==member_id)&(db[doc]["roleType_id"]==roleType_id)):
                        exist=1
                        existedidofRelat=db[doc]["_id"]
                        break
                    else:
                        exist=0
                except:
                    pass
            if(exist==0):
                newid="idRelat-"+str(random.randrange(999999999999))+str(datetime.timestamp(datetime.now())).replace(".","T")+str(random.randrange(999999999999))
                data={"_id":newid, "id":newid, "users_id":str(member_id), "groups_id":grpID, "roleType_id":roleType_id, "type":"relation"}
                insert_document(data)
            if(exist==1):
                find_first(existedidofRelat)
					

    def RemoveMember(self, member_id):
        for doc in db:
            try:
                if((db[doc]["type"]=="relation")&(db[doc]["users_id"]==member_id)&(db[doc]["groups_id"]==self.id)):
                    del_doc(db[doc])
            except:
                pass

    def UpdateData(self):
        newdata={
            "name":self.name,
            "groupType":self.groupType
        }
        puvodni=find_first(self.id)
        puvodni=puvodni.copy()
        for k in newdata.keys():
            if newdata[k] is None:
                newdata[k]=puvodni[k]
        puvodni.update(newdata)
        db.save(puvodni)

    def Del(self):
        grpID=self.id
        for doc in db:
            try:
                if((db[doc]["type"]=="relation")&(db[doc]["groups_id"]==grpID)):
                    db.delete(db[doc])
            except:
                pass
        db.delete(db[grpID])

class GroupType:
	def __init__(self, name = None):
		self.id = None
		self.name = name

	def Load(self, grptypeID):
		self.id=grptypeID
		v=find_first(grptypeID)
		v=v.copy()
		self.name=v["name"]

	def AddToDB(self):
		data={
			"_id":None,
			"id":None,
			"name":str(self.name)
		}
		self.id="idGrpType-"+str(random.randrange(999999999999))+str(datetime.timestamp(datetime.now())).replace(".","T")+str(random.randrange(999999999999))
		data["_id"]=self.id
		data["id"]=data["_id"]
		insert_document(data)

	def UpdateData(self):
		newdata={
			"name":self.name
		}
		puvodni=find_first(self.id)
		puvodni=puvodni.copy()
		for k in newdata.keys():
			if newdata[k] is None:
				newdata[k]=puvodni[k]
		puvodni.update(newdata)
		db.save(puvodni)

	def Del(self): #odstranit pouze Group Type a ne odstranovat spojeni s Group (podle predlohy k mereni !) (jinak by se asi odstranila i group)
		GrpTypeID=self.id
		db.delete(db[GrpTypeID])
		

class Membership: 
    def __init__(self, roleType_id = None, group_id = None):
        self.roleType_id = roleType_id 
        self.group_id = group_id 

    def GetGroup(self):
        GRid=self.group_id
        vys=find_first(GRid)
        vys=vys.copy()

        grp=Group()
        grp.Load(vys["_id"])
        return (grp)

    def GetRoleType(self):
        RTid=self.roleType_id
        vys=find_first(RTid)
        vys=vys.copy()

        roletyp=RoleType()
        roletyp.Load(vys["_id"])
        return (roletyp)


class Person:
	def __init__(self, name = None, surname = None, age = None):
		self.id = None
		self.name = name
		self.surname = surname
		self.age = age

	def Load(self, user_id):
		self.id = user_id
		data=find_first(user_id)
		data=data.copy()
		self.age=data["age"]
		self.surname=data["surname"]
		self.name = data["name"]

	def GetMemberships(self):
		personID=self.id
		vys=[]
		out=[]
		for doc in db:
			try:
				if((db[doc]["type"]=="relation") & (db[doc]["users_id"]==personID)):
					prvek=find_first(db[doc]["_id"])
					prvek=prvek.copy()
					vys.append(prvek)
				else:
					pass
			except:
				pass
		for v in vys:
			tmp = Membership()
			tmp.group_id=v["groups_id"]
			tmp.roleType_id=v["roleType_id"]
			out.append(tmp)
		return(out)

	def AddToDB(self):
		data={
			"_id":None,
			"id":None,
			"name":str(self.name),
			"surname":str(self.surname),
			"age":str(self.age),
            "type":"user"
		}
		self.id="idUsr-"+str(random.randrange(999999999999))+str(datetime.timestamp(datetime.now())).replace(".","T")+str(random.randrange(999999999999))
		data["_id"]=self.id
		data["id"]=data["_id"]
		insert_document(data)

	def UpdateData(self):
		newdata={
			"name":self.name,
			"surname":self.surname,
			"age":self.age
		}
		puvodni=find_first(self.id)
		puvodni=puvodni.copy()
		for k in newdata.keys():
			if newdata[k] is None:
				newdata[k]=puvodni[k]
		puvodni.update(newdata)
		db.save(puvodni)
		
	def Del(self):
		personID=self.id
		for doc in db:
			try:
				if((db[doc]["type"]=="relation")&(db[doc]["users_id"]==personID)):
					db.delete(db[doc])
			except:
				pass
		db.delete(db[personID])

class RoleType:
    def __init__(self, name = None):
        self.id = None
        self.name = name

    def Load(self, roletypeID):
        self.id=roletypeID
        v=find_first(roletypeID)
        v=v.copy()
        self.name=v["name"]

    def AddToDB(self):
        data={
            "_id":None,
            "id":None,
            "name":str(self.name)
        }
        self.id="idRol-"+str(random.randrange(999999999999))+str(datetime.timestamp(datetime.now())).replace(".","T")+str(random.randrange(999999999999))
        data["_id"]=self.id
        data["id"]=data["_id"]
        insert_document(data)

    def UpdateData(self):
        newdata={
			"name":self.name
        }
        puvodni=find_first(self.id)
        puvodni=puvodni.copy()
        for k in newdata.keys():
            if newdata[k] is None:
                newdata[k]=puvodni[k]
        puvodni.update(newdata)
        db.save(puvodni)

    def Del(self): # odstraneni pouze roleType a ne vazeb ( zase podle zadani k mereni !) (Jinak by se odstranili nebo vyresili i vazby !)
        db.delete(db[self.id])

#-------program-databaze-add-default-data--------#


dataPersonLoad=PersonDataFun()
dataRoleLoad=RoleDataFun()
dataGroupLoad=GroupDataFun()
dataGroupTypesLoad=GroupTypesDataFun()
dataRelationLoad=Relations()

#PersonDataFun, RoleDataFun, GroupDataFun, GroupTypesDataFun, Relations

print(".............vkladam data do databaze.............")
for data in dataPersonLoad:
    if "_id" in data:
        insert_document(data)
    else:
        data["_id"]=data["id"]
        insert_document(data)
print("Persons data vlozena! ")

for data in dataRoleLoad:
    if "_id" in data:
        insert_document(data)
    else:
        data["_id"]=data["id"]
        insert_document(data)
print("Roles data vlozena! ")

for data in dataGroupLoad:
    if "_id" in data:
        insert_document(data)
    else:
        data["_id"]=data["id"]
        insert_document(data)
print("Group ulozeny do dbs")

for data in dataGroupTypesLoad:
    if "_id" in data:
        insert_document(data)
    else:
        data["_id"]=data["id"]
        insert_document(data)
print("Group types ulozeny do dbs")

for data in dataRelationLoad:
    if "_id" in data:
        insert_document(data)
    else:
        data["_id"]=data["id"]
        insert_document(data)
print("Relations vytvoreny v dbs")
