from graphene import ObjectType, String, Field, List
import graphene
from conect import print_all,find_first,insert_document
from models import CourseType,UsrType

from datetime import datetime

######----------GQL-QUERY--------#######

class Query(ObjectType):
    get_course = Field(CourseType, id = String(required=True))
    user=List(UsrType)

    course_list = {}
    
    def resolve_get_course(root, info,id): #vypise prvniho nalezenoho podle zadaneho id 
        course_list = find_first(id) #'id#2022-05-10 06:22:44.414852#id'
        return course_list 

    def resolve_user(root, info): #vypise vsechny prvky(dokumenty) z databaze(list of dictionaries)
        usr=print_all()
        result=list()
        n=1
        for prvky in usr:
            result.append(usr['data'+str(n)])
            n=n+1
        return result
    
#####------------GQL-MUTATIONS------######

class CreateCourseInput(graphene.InputObjectType):
    _id=String(required=True)
    title=String(required=False)
    instructor=String(required=False)
    publish_date=String(default=datetime.now()) #graphene.DateTime .... ale nefunguje je potreba se na to vic podivat do hloubky

    def asDict(self):
        return {
            '_id':self._id,
            'title':self.title,
            'instructor':self.instructor,
            'publish_date':self.publish_date
        }

class CreateCourse(graphene.Mutation):
    class Arguments:
        course = CreateCourseInput(required=False)

    ok=graphene.Boolean()
    result=graphene.Field(CourseType)

    def mutate(parent, info, course=None):
        course_list = {}
        course_listdef={"_id":"defultID", "title": "defaulttitle", "instructor": "defaultinstructor", "publish_date": ""} #, "publish_date": "" + datetime.now + "" 
        course_list=course_listdef.copy()
        course_list.update(course)
        res=insert_document(course_list)
        return CreateCourse(ok=True, result=res)
    pass


class Mutations(ObjectType):
    create_course = CreateCourse.Field()
