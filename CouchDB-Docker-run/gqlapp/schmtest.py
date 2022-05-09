from cgitb import reset
from graphene import String, ObjectType
import graphene

class CourseType(ObjectType):
    _id = String(required=True)
    title = String(required=True)
    instructor = String(required=True)
    publish_date = String()
    
    #coursetypes=graphene.List(CourseType)

    #def resolve_coursetypes(parent,info):
    #    courseType_id=parent._id
    #    result=[]
    #    return result