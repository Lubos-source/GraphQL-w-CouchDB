import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


from conect import conectToCouch
#from schemas import Query,Mutation
from schmtest import CourseType, UsrType
from graphene import ObjectType, List, String, Schema, Field, Mutation
from conect import print_all,insert_document,find_first


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
"""
class CreateCourse(Mutation):
    class Arguments:
        course = CreateCourseInput(required=True)

    ok=graphene.Boolean()
    result=graphene.Field(CourseType)

    def mutate(parent, info, course):
        course_list = {}
        course_list={"_id":"ajdiNatvrdo", "title": "titleTestNaTvrdo", "instructor": "instructorTvrdej"}
        insert_document(course_list,"NejakyID222")
        return CreateCourse(ok=True, result=course_list)
    pass
"""

#course_list = {'data':{}}
class Query(graphene.ObjectType):
    get_course = graphene.Field(CourseType, id = graphene.String(required=True))
    user=graphene.List(UsrType)

    course_list = {}
    
    def resolve_get_course(root, info,id): #vypise prvniho nalezenoho podle zadaneho id 
        course_list = find_first(id) #'id#2022-05-10 06:22:44.414852#id'
        """
        n=1
        for prvky in course_list:
            return(course_list['data'+str(n)])
            n=n+1
        """
        return course_list 

    def resolve_user(root, info): #vypise vsechny prvky(dokumenty) z databaze(list of dictionaries)
        usr=print_all()
        result=list()
        n=1
        for prvky in usr:
            result.append(usr['data'+str(n)])
            n=n+1
        return result
    
"""
class Mutations(ObjectType):
    create_course = CreateCourse.Field()
"""


#db = conectToCouch() #zde to neni potreba ? je to nutne u gql, kde budem delat mutace a jine operace si myslim

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "hello testing FASTAPI"}

#app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))


app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query))) #, mutation=Mutations