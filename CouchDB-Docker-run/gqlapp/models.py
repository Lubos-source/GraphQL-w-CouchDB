from graphene import String,List
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

    # groups = List(lambda: Group)   #???? neco takoveho asi :)
    """def resolve_groups(parent, info):
            session = extractSession(info)
            personRecord = session.query(PersonModel).get(parent.id)
            return personRecord.groups
"""

class Group(graphene.ObjectType):
    id=String()                     # 23-5KB, FVT, FVL, FVZ, ucitel_UO, student_UO, K-209,
    name=String()

    #NM - GROUP - PERSON
    members = List(UsrType)     #Mozna udelat jen List of IDs a kdyz se tvori skupina tak vsechny ID ktere zde jsou tak aktualizovat aby meli ID dane ksupiny v sobe (UPDATE)
                                #To stejne pokud se vytvori uzivatel ktery bude mit ID skupiny tak zkontrolovat pripdane UPDATE dane skupiny jestli ma v members ID uzivatele

    #1N - GROUPTYPE - GROUP
    # grouptype = Field(lambda: GroupType)
    """def resolve_grouptype(parent, info):
            session = extractSession(info)
            groupRecord = session.query(GroupModel).get(parent.id)
            return groupRecord.group_type
"""

class GroupType(graphene.ObjectType):
    id=String()                     #studijni skupina, skolni pluk, katedra, fakulta, ucitele, studenti,
    name=String()
    #1N - GROUPTYPE - GROUP
    # groups = List(Group)

    """def resolve_groups(parent, info):
            session = extractSession(info)
            grouptypeRecord = session.query(GroupTypeModel).get(parent.id)
            return grouptypeRecord.groups
"""

class Role(graphene.ObjectType):
    id=String()                     #student, ucitel, (v kazde skupine ve ktere je ma nejakou roli)
    name=String()

    #NM - GROUP - PERSON
    members = List(UsrType)
    # groups = List(lambda: Group)

class RoleType(graphene.ObjectType):
    id=String()                     #??? typ role ???? nwm
    name=String()

    #NM - GROUP - PERSON
    members = List(UsrType)

class Response(graphene.ObjectType):
    name=String()
    message=String()