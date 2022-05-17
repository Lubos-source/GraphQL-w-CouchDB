from unittest import result
from graphene import ObjectType, String, Field, List
import graphene
from conect import print_all,find_first,insert_document,update_user,del_doc
from models import UsrType, Response #,Group,GroupType

from datetime import datetime
##########################################
######----------GQL-QUERY----------#######
##########################################
class Query(ObjectType):
    get_user = Field(UsrType, id = String(required=True))
    users=List(UsrType)

    # group = Field(Group, id = ID(required=True))
    # grouptype = Field(GroupType, id = ID(required=True))

    user_list = {}
    
    def resolve_get_user(root, info,id): #vypise prvniho nalezenoho podle zadaneho id 
        user_list = find_first(id) #'id#2022-05-10 06:22:44.414852#id'
        return user_list 

    def resolve_users(root, info): #vypise vsechny prvky(dokumenty) z databaze(list of dictionaries)
        usr=print_all()
        result=list()
        n=1
        for prvky in usr:
            result.append(usr['data'+str(n)])
            n=n+1
        return result

    """def resolve_group(root, info, id):
        session = extractSession(info)
        return session.query(GroupModel).get(id)"""

    """    def resolve_grouptype(root, info, id):
            session = extractSession(info)
            return session.query(GroupTypeModel).get(id)"""
    
##############################################    
#####------------GQL-MUTATIONS------------####
##############################################

#######-USER-create-#######

class CreateUserInput(graphene.InputObjectType):
    _id=String(required=False)
    name=String(required=False)
    surname=String(required=False)
    address=String(required=False)
    email=String(required=False, default="default@email.com")
    publish_date=String(default=datetime.now()) #graphene.DateTime .... ale nefunguje je potreba se na to vic podivat do hloubky

    def asDict(self):
        return {
            '_id':self._id,
            'name':self.name,
            'surname':self.surname,
            'address':self.address,
            'email':self.email,
            'publish_date':self.publish_date
        }

class CreateUser(graphene.Mutation):
    class Arguments:
        userC = CreateUserInput(required=False)

    ok=graphene.Boolean()
    result=graphene.Field(UsrType)

    def mutate(parent, info, userC=None):
        user_list = {}
        user_listdef={"_id":"defultID", "name": "defaultname", "surname": "defaultsurname","address":"defAdress","email":"def@email.com", "publish_date": ""} #, "publish_date": "" + datetime.now + "" 
        user_list=user_listdef.copy()
        user_list.update(userC)
        res=insert_document(user_list)
        return CreateUser(ok=True, result=res)
    pass

####-USER-update####                            #DODELAT: pokud se v dbs nenachazi tak vytvorit nebo poslat chybovouhlasku !!!!!!
class UpdateUser(graphene.Mutation):
    class Arguments:
        id=String(required=True)
        UserUP= CreateUserInput(required=False)
    
    ok= graphene.Boolean()
    result=graphene.Field(UsrType)

    def mutate(parent,info, id, UserUP={}):            #nevim proc ale "info" zde musi byt i kdyz se nepouzije ... jinak nejede (NonType Error)

        user=update_user(UserUP, id)
        res=find_first(id)
        return UpdateUser(ok=True,result=res)

####-USER-delete-####
class DeleteUser(graphene.Mutation):
    class Arguments:
        id=String(required=True)

    ok=graphene.Boolean()
    result=graphene.Field(Response)

    def mutate(parent, info, id):
        delection=del_doc(id)
        return DeleteUser(ok=True,result=delection)

#######-GROUP-create-########

class CreateGroupInput(graphene.InputObjectType):
    _id=String(required=True)
    name=String(required=False)
    
    def asDict(self):
        return {
            '_id':self._id,
            'name':self.name
        }


class CreateGroup(graphene.Mutation):
    class Arguments:
        groupC = CreateGroupInput(required=False)

    ok=graphene.Boolean()
    result=graphene.Field(UsrType)

    def mutate(parent, info, groupC=None):
        group_list = {}
        group_listdef={"_id":"defultGroupID", "name": "defaultnameOfGROUP"}
        group_list=group_listdef.copy()
        group_list.update(groupC)
        res=insert_document(group_list)
        return CreateGroup(ok=True, result=res)
    pass


class Mutations(ObjectType):
    create_user = CreateUser.Field()
    create_group = CreateGroup.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

