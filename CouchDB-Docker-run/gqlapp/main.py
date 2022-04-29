import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


from conect import conectToCouch
from schemas import Query,Mutation
from ../conection-jupy-funcni import couchDbLogin


#db = conectToCouch() #zde to neni potreba ? je to nutne u gql, kde budem delat mutace a jine operace si myslim

app = FastAPI()

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))

#app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=PostMutations)))