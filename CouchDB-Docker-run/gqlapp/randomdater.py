####################################################
##---------HARD-NO-CHANGE-VALUES------------------##
####################################################

def GroupTypeDataFun():
    datagrptype=[
    {"_id":"idGrT-0", "name":"all", "type":"group_type"},
    {"_id":"idGrT-1", "name":"katedra", "type":"group_type"},
    {"_id":"idGrT-2", "name":"fakulta", "type":"group_type"},
    {"_id":"idGrT-3", "name":"studijni skupina", "type":"group_type"},
    {"_id":"idGrT-4", "name":"skolni pluk", "type":"group_type"}
    ]
    return(datagrptype)

def RoleDataFun():
    datarole=[
    {"_id":"idR-0", "name":"everybody", "type":"role"},
    {"_id":"idR-1", "name":"ucitel", "type":"role"},
    {"_id":"idR-2", "name":"student", "type":"role"},
    {"_id":"idR-3", "name":"vedouci katedry", "type":"role"}
    ]
    return(datarole)

def GroupDataFun():
    datagroup=[
    {"_id":"Group-all-users", "name":"All Users", "type":"group", "members":[],"groupType":["idGrT-0"]}
    ]
    return(datagroup)