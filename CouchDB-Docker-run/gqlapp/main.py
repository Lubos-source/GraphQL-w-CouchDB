from dis import Instruction
from typing_extensions import Required
from unittest import result
import graphene
from fastapi import FastAPI
#from numpy import require
from starlette.graphql import GraphQLApp


from conect import conectToCouch
#from schemas import Query,Mutation
from schmtest import CourseType
from graphene import ObjectType, List, String, Schema, Field, Mutation
from conect import print_all,insert_document


###zkouska tvorby GQL - zatim nefunguje -_-
"""
class CreateCourseInput(graphene.InputObjectType):
    _id=String(required=True)
    title=String(required=False)
    instructor=String(required=False)

    def asDict(self):
        return {
            '_id':self._id,
            'title':self.title,
            'instructor':self.instructor
        }
"""


class CreateCourse(Mutation):
    #class Arguments:
       # course = CreateCourseInput(required=True)

    ok=graphene.Boolean()
    result=graphene.Field(CourseType)

    def mutate(parent, info, course):
        course_list = {}
        course_list={"_id":"ajdiNatvrdo", "title": "titleTestNaTvrdo", "instructor": "instructorTvrdej"}
        insert_document(course_list,"NejakyID222")
        return CreateCourse(ok=True, result=course_list)
    pass



class Query(ObjectType):
    course_list = {}
    get_course = Field(CourseType, _id=graphene.ID(required=True))
    def resolve_get_course(self, **kwargs):
#zatim vrati posledni dokument v databazi - ale funguje :) chyba ve funkci print_all - prepisuje dictionary. Ale list dictionaries ani dict in dict nefunguje musi se to nejak vyresit
        course_list = print_all()
        return course_list
    

class Mutations(ObjectType):
    create_course = CreateCourse.Field()



#db = conectToCouch() #zde to neni potreba ? je to nutne u gql, kde budem delat mutace a jine operace si myslim

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "hello testing FASTAPI"}

#app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))


app.add_route("/graphql", GraphQLApp(schema=Schema(query=Query, mutation=Mutations)))