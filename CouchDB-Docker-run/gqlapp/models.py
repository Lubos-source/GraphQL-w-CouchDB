from graphene import String,List
import graphene


#########--------GQL models:----------#########

class UsrType(graphene.ObjectType):
    _id = String()
    type="user"
    name = String()
    surname = String()
    publish_date = String()
    address=String() 
    email= String()

    groups = List(lambda: Group)   #???? neco takoveho asi :)
    
    #{"_id": "ID", "_rev": "......", "type": "user", "name": "NAME", "surname": "SURNAME", "address": "ADRESA", \
    # "email": "EMAIL@email.cz", "groups": [{"grpid": "ID1", "grprole":"idR1",},{"grpid": "ID2", "grprole":"idR2",},...],"publish_date": "2022-06-02 18:59:36.778196"}

    #grprole=id role v dane skupině

    #2. návrh 01.06.2022 - neukláadat celé objekty, protože se zacyklí a zadrbe celou databázi, moc místa ! takže ukládat jen ID a pak při query 
    # použít find(ID) ktere se vlozi do vysledku, mohlo by asi fungovat :)

class Group(graphene.ObjectType):
    _id=String()                     # 23-5KB, FVT, FVL, FVZ, ucitele_UO, studenti_UO, K-209,
    type="group"
    name=String()
    publish_date = String()

    members = List(UsrType)

    groupType=List(lambda: GroupType)

    #{"_id":"ID", "type":"group", "name":"NAME", "publish_data":"03.06.2022", "members":["ID1", "ID2", "ID3",...], "groupType":["idG1",...]}

class GroupType(graphene.ObjectType):
    _id=String()                     #studijni skupina, skolni pluk, katedra, fakulta
    type="group_type"
    name=String()
   
   #{"_id":"idGrT-0","name":"all","type":"group_type"}
   #{"_id":"idGrT-1","name":"katedra","type":"group_type"}
   #{"_id":"idGrT-2","name":"fakulta","type":"group_type"}
   #{"_id":"idGrT-3","name":"studijni skupina","type":"group_type"}
   #{"_id":"idGrT-4","name":"skolni pluk","type":"group_type"}

class Role(graphene.ObjectType):
    _id=String()                     #student, ucitel, vedouci katedry
    type="role"
    name=String()

    #{"_id:""idR-0","name":"everybody","type":"role"}
    #{"_id:""idR-1","name":"ucitel","type":"role"}
    #{"_id:""idR-2","name":"student","type":"role"}
    #{"_id:""idR-3","name":"vedouci katedry","type":"role"}
    
    #members = List(UsrType)

class Response(graphene.ObjectType):
    name=String()
    type="response"
    message=String()



########################################################################
## */*-------------nepouzito ----> navic: ??----------------------*/* ##
########################################################################
class RoleType(graphene.ObjectType):
    _id=String()                     #??? typ role ???? nevim co by to mohlo byt?
    type="role_type"
    name=String()

    #members = List(UsrType)
