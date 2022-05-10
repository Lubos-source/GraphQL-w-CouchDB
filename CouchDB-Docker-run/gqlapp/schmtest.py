from graphene import String, ObjectType
import graphene


#GQL model:

class CourseType(graphene.ObjectType):
    _id = String()
    title = String()
    instructor = String() #required=False
    publish_date = String()
    
    #coursetypes=graphene.List(CourseType)

    #def resolve_coursetypes(parent,info):
    #    courseType_id=parent._id
    #    result=[]
    #    return result

class UsrType(graphene.ObjectType):
    _id = String()
    title = String()
    instructor = String()
    publish_date = String()