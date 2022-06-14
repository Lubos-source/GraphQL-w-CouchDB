####################################################
##---------HARD-NO-CHANGE-VALUES------------------##
####################################################

def PersonDataFun():
    datagrptype=[
    {"id":"idUsr-1", "name":"Timmy", "surname":"Trumpet", "age":"35", "type":"user"},
    {"id":"idUsr-2", "name":"Ava", "surname":"Max", "age":"25", "type":"user"},
    {"id":"idUsr-3", "name":"Becky", "surname":"Hill", "age":"30", "type":"user"},
    {"id":"idUsr-4", "name":"Dua", "surname":"Lipa", "age":"28", "type":"user"},
    {"id":"idUsr-5", "name":"Jan", "surname":"Veliky", "age":"60", "type":"user"},
    {"id":"idUsr-6", "name":"Petr", "surname":"Maly", "age":"25", "type":"user"},
    {"id":"idUsr-7", "name":"Pavel", "surname":"Novotny", "age":"42", "type":"user"},
    {"id":"idUsr-8", "name":"David", "surname":"Guetta", "age":"40", "type":"user"}
    ]
    return(datagrptype)

def RoleDataFun():
    datarole=[
    {"id":"idRol-0", "name":"everybody", "type":"role"},
    {"id":"idRol-1", "name":"ucitel", "type":"role"},
    {"id":"idRol-2", "name":"student", "type":"role"},
    {"id":"idRol-3", "name":"vedouci katedry", "type":"role"}
    ]
    return(datarole)

def GroupDataFun():
    datagroup=[
    #{"_id":"Group-all-users", "name":"All Users", "type":"group", "members":[],"groupType":["idGrT-0"]},
    {"id":"idGrp-1", "name":"FVT", "groupType":"idGrpType-1", "type":"group"},
    {"id":"idGrp-2", "name":"FVL", "groupType":"idGrpType-1", "type":"group"},
    {"id":"idGrp-3", "name":"23-5KB", "groupType":"idGrpType-3", "type":"group"},
    {"id":"idGrp-4", "name":"21-5TPVO", "groupType":"idGrpType-3", "type":"group"},
    {"id":"idGrp-5", "name":"Katedra informatiky a kybernetickych operaci", "groupType":"idGrpType-2", "type":"group"},
    {"id":"idGrp-6", "name":"Katedra radiolokace", "groupType":"idGrpType-2", "type":"group"}
    ]
    return(datagroup)

def GroupTypesDataFun():
    dataGroupTypes=[
    {"id":"idGrpType-1", "name":"fakulta", "type":"grouptype"},
    {"id":"idGrpType-2", "name":"katedra", "type":"grouptype"},
    {"id":"idGrpType-3", "name":"ucebni skupina", "type":"grouptype"}
    ]
    return(dataGroupTypes)

def Relations():
    data_relation = [
    {"id":"idRelat-1", "users_id":"idUsr-1", "groups_id":"idGrp-1", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-2", "users_id":"idUsr-1", "groups_id":"idGrp-3", "roleType_id":"idRol-2", "type":"relation"},
    {"id":"idRelat-3", "users_id":"idUsr-1", "groups_id":"idGrp-5", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-4", "users_id":"idUsr-2", "groups_id":"idGrp-1", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-5", "users_id":"idUsr-2", "groups_id":"idGrp-6", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-6", "users_id":"idUsr-3", "groups_id":"idGrp-1", "roleType_id":"idRol-2", "type":"relation"},
    {"id":"idRelat-7", "users_id":"idUsr-3", "groups_id":"idGrp-3", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-8", "users_id":"idUsr-4", "groups_id":"idGrp-1", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-9", "users_id":"idUsr-4", "groups_id":"idGrp-4", "roleType_id":"idRol-3", "type":"relation"},
    {"id":"idRelat-10", "users_id":"idUsr-5", "groups_id":"idGrp-5", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-11", "users_id":"idUsr-6", "groups_id":"idGrp-5", "roleType_id":"idRol-2", "type":"relation"},
    {"id":"idRelat-12", "users_id":"idUsr-7", "groups_id":"idGrp-5", "roleType_id":"idRol-1", "type":"relation"},
    {"id":"idRelat-13", "users_id":"idUsr-8", "groups_id":"idGrp-2", "roleType_id":"idRol-2", "type":"relation"}
    ]
    return(data_relation)