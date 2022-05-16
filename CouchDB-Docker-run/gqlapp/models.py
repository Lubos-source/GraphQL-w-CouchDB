from graphene import String
import graphene


#########--------GQL models:----------#########
"""
class CourseType(graphene.ObjectType):
    _id = String()
    name = String()
    surname = String() #required=False
    publish_date = String()
    """
    #coursetypes=graphene.List(CourseType) # v pripade propojeni prvku v dbs ("asi odkazy v databazi")

    #def resolve_coursetypes(parent,info):
    #    courseType_id=parent._id
    #    result=[]
    #    return result

class UsrType(graphene.ObjectType):
    _id = String()
    name = String()
    surname = String()
    publish_date = String()
    address=String() 
    email= String()

    #groups = List(lambda: Group)   ???? neco takoveho asi :)
    """def resolve_groups(parent, info):
            session = extractSession(info)
            personRecord = session.query(PersonModel).get(parent.id)
            return personRecord.groups
"""

class Group(graphene.ObjectType):
    id=String()
    name=String()

    #NM - GROUP - PERSON
    # members = List(Person)
    #1N - GROUPTYPE - GROUP
    # grouptype = Field(lambda: GroupType)
    """def resolve_grouptype(parent, info):
            session = extractSession(info)
            groupRecord = session.query(GroupModel).get(parent.id)
            return groupRecord.group_type
"""

class GroupType(graphene.ObjectType):
    id=String()
    name=String()
    #1N - GROUPTYPE - GROUP
    # groups = List(Group)

    """def resolve_groups(parent, info):
            session = extractSession(info)
            grouptypeRecord = session.query(GroupTypeModel).get(parent.id)
            return grouptypeRecord.groups
"""
