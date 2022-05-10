from graphene import String
import graphene


#########--------GQL models:----------#########

class CourseType(graphene.ObjectType):
    _id = String()
    title = String()
    instructor = String() #required=False
    publish_date = String()
    
    #coursetypes=graphene.List(CourseType) # v pripade propojeni prvku v dbs ("asi odkazy v databazi")

    #def resolve_coursetypes(parent,info):
    #    courseType_id=parent._id
    #    result=[]
    #    return result

class UsrType(graphene.ObjectType):
    _id = String()
    title = String()
    instructor = String()
    publish_date = String()