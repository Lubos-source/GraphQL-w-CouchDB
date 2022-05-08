import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


from conect import conectToCouch
#from schemas import Query,Mutation
from schmtest import CourseType
from graphene import ObjectType, List, String, Schema, Field, Mutation
from conect import print_all,insert_document


###zkouska tvorby GQL - zatim nefunguje -_-

class CreateCourse(Mutation):
    course = Field(CourseType)

    class Arguments:
        _id = String(required=True)
        title = String(required=True)
        instructor = String(required=True)

    def mutate(self, info, id, title, instructor):
        course_list = None
        course_list.insert_document({"id": id, "title": title, "instructor": instructor},"ajdii")
        return CreateCourse(course=course_list[-1])



class Query(ObjectType):
    course_list = None
    get_course = List(CourseType)
    def resolve_get_course(self, info, **kwargs):
        course_list = print_all()
        return course_list
    
    #return course_list

class Mutation(ObjectType):
    create_course = CreateCourse.Field()



#db = conectToCouch() #zde to neni potreba ? je to nutne u gql, kde budem delat mutace a jine operace si myslim

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "hello testing FASTAPI"}

#app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))


app.add_route("/graphql", GraphQLApp(schema=Schema(query=Query, mutation=Mutation)))