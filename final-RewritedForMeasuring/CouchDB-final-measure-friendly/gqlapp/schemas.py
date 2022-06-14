from re import X
from unittest import result
from graphene import ObjectType, String, Field, List
import graphene
from conect import connectToDatabase,DB_Name_To_Create
#from models import Person, Response, Group, GroupType, RoleType
import conect

from datetime import datetime

dbname=DB_Name_To_Create

class Person(graphene.ObjectType):
    id = String()
    type="user"
    name = String()
    surname = String()
    age= String()
    
    membership = List(lambda: Membership)  

    def resolve_membership(parent, info):
        newl=parent.GetMemberships()            # ZDE PROBLEM  na ktery mi tvalo prijit !!!! furt jsem volal conect.Person.GetMemberships() ale má zde být parent.GetMembership() 
        return (newl)


class Group(graphene.ObjectType):
    id=String()                     
    type="group"
    name=String()
   
    members = List(Person)
    groupType=graphene.Field(lambda: GroupType)

    def resolve_members(parent, info):
        vys=parent.GetMembers()
        return(vys)

    def resolve_groupType(parent, info):
        vys=parent.GetGroupType()
        return(vys)


class GroupType(graphene.ObjectType):
    id=String()                    
    type="group_type"
    name=String()


class RoleType(graphene.ObjectType):
    id=String()                    
    type="role_type"
    name=String()


class Membership(graphene.ObjectType):
    roleType = graphene.Field(lambda: RoleType)
    group = graphene.Field(lambda: Group)

    def resolve_roleType(parent,info):
        n=parent.GetRoleType()
        return(n)

    def resolve_group(parent,info):
        n=parent.GetGroup()
        return(n)

class Response(graphene.ObjectType):
    name=String()
    type="response"
    message=String()


##########################################
######----------GQL-QUERY----------#######
##########################################
class Query(ObjectType):
    person = graphene.Field(Person, id = String(required=True))
    group = graphene.Field(Group, id = String(required=True))
    groupType = graphene.Field(GroupType, id = String(required=True))
    roleType = graphene.Field(RoleType, id = String(required=True))

    def resolve_person(root, info, id): 
        person=conect.Person()
        person.Load(id)
        return person

    def resolve_group(root, info, id): 
        group=conect.Group()
        group.Load(id)
        return group

    def resolve_groupType(root, info, id): 
        group=conect.GroupType()
        group.Load(id)
        return group

    def resolve_roleType(root, info, id): 
        group=conect.RoleType()
        group.Load(id)
        return group

##############################################    
#####------------GQL-MUTATIONS------------####
##############################################       

class CreatePerson(graphene.Mutation):
    person = graphene.Field(Person) 

    class Arguments:
        name = graphene.String()
        surname = graphene.String()
        age = graphene.String()

    def mutate(parent, info, name, surname, age):
        person = conect.Person()

        person.name=name
        person.surname=surname
        person.age=age

        person.AddToDB()
        return CreatePerson(person=person)

class CreateGroup(graphene.Mutation):
    group = graphene.Field(Group)

    class Arguments:
        name = graphene.String()
        groupTypeID = graphene.String()

    def mutate(parent, info, name, groupTypeID):
        group = conect.Group()
        group.name = name
        group.groupType = groupTypeID
        group.AddtoDB()
        return CreateGroup(group=group)

class CreateGroupType(graphene.Mutation):
    groupType = graphene.Field(GroupType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        groupType = conect.GroupType()
        groupType.name = name
        groupType.AddToDB()
        return CreateGroupType(groupType=groupType)

class CreateRoleType(graphene.Mutation):
    roleType = graphene.Field(RoleType)

    class Arguments:
        name = graphene.String()

    def mutate(parent, info, name):
        roleType = conect.RoleType()
        roleType.name = name
        roleType.AddToDB()
        return CreateRoleType(roleType=roleType)

class AddUserToGroup(graphene.Mutation): 
    group = graphene.Field(Group)
    person = graphene.Field(Person)

    class Arguments:
        groupID = graphene.String()
        userID = graphene.String()
        roleTypeID = graphene.String()

    def mutate(parent, info, groupID, userID, roleTypeID):
        group = conect.Group()
        group.Load(groupID)
        group.AddMember(userID, roleTypeID)
        user = conect.Person()
        user.Load(userID)
        return AddUserToGroup(group = group, person = user)

class RemoveUserFromGroup(graphene.Mutation):
    group = graphene.Field(Group)
    person = graphene.Field(Person)

    class Arguments:
        groupID = graphene.String()
        userID = graphene.String()

    def mutate(parent, info, groupID, userID):
        gr = conect.Group()
        gr.Load((groupID))
        gr.RemoveMember((userID))
        per = conect.Person()
        per.Load((userID))
        return RemoveUserFromGroup(group = gr, person = per)

class UpdatePerson(graphene.Mutation):
    person = graphene.Field(Person)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        surname = graphene.String()
        age = graphene.String()

    def mutate(parent, info, id, name, surname, age):
        person = conect.Person()
        person.Load((id))
        person.name = name
        person.surname = surname
        person.age = age
        person.UpdateData()
        person.Load(id)
        return UpdatePerson(person = person)

class UpdateGroup(graphene.Mutation):  #Pokud zada neplatny group Type tak pak pri hledani skupiny k vraceni error-> nenajde grptype v dbs!!!
    group = graphene.Field(Group)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()
        groupTypeID = graphene.String()

    def mutate(root, info, id, name, groupTypeID):
        group = conect.Group()
        group.Load((id))
        group.name = name
        group.groupType = groupTypeID
        group.UpdateData()
        group.Load(id)
        return UpdateGroup(group = group)

class UpdateGroupType(graphene.Mutation):
    groupType = graphene.Field(GroupType)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()

    def mutate(parent, info, id, name):
        grptype = conect.GroupType()
        grptype.Load((id))
        grptype.name = name
        grptype.UpdateData()
        grptype.Load(id)
        return UpdateGroupType(groupType = grptype)

class UpdateRoleType(graphene.Mutation):
    roleType = graphene.Field(RoleType)

    class Arguments:
        id = graphene.ID(required = True)
        name = graphene.String()

    def mutate(parent, info, id, name):
        roletype = conect.RoleType()
        roletype.Load((id))
        roletype.name = name
        roletype.UpdateData()
        roletype.Load(id)
        return UpdateRoleType(roleType = roletype)

class DelPerson(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        db=connectToDatabase(dbname)
        if id in db:
            person = conect.Person()
            person.Load((id))
            person.Del()
        return DelPerson(status = "ok")

class DelGroup(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        db=connectToDatabase(dbname)    #kvuli tomu kdyz uz je prvek odstranen at se vyhneme chybe -> vrati OK (neodstrani) ale v dbs neni takze OK
        if id in db:
            gr = conect.Group()
            gr.Load((id))
            gr.Del()
        return DelGroup(status = "ok")

class DelGroupType(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        db=connectToDatabase(dbname)
        if id in db:
            grptype = conect.GroupType()
            grptype.Load((id))
            grptype.Del()
        return DelGroupType(status = "ok")

class DelRoleType(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.ID(required = True)

    def mutate(parent, info, id):
        db=connectToDatabase(dbname)
        if id in db:
            roltype = conect.RoleType()
            roltype.Load((id))
            roltype.Del()
        return DelRoleType(status = "ok")

class Mutations(ObjectType):
    create_person = CreatePerson.Field()
    create_group = CreateGroup.Field()
    create_group_type = CreateGroupType.Field()
    create_role_type = CreateRoleType.Field()

    add_user_to_group = AddUserToGroup.Field()
    remove_user_from_group = RemoveUserFromGroup.Field()
    
    update_person = UpdatePerson.Field()
    update_group = UpdateGroup.Field()
    update_group_type = UpdateGroupType.Field()
    update_role_type = UpdateRoleType.Field()

    del_person = DelPerson.Field()
    del_group = DelGroup.Field()
    del_group_type = DelGroupType.Field()
    del_role_type = DelRoleType.Field()
