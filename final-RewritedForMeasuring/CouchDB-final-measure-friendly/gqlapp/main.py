import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from schemas import Query,Mutations


app = FastAPI()

@app.get("/")
async def root():
    return{"message": "hello testing FASTAPI",
    "nextmove": "please go to /graphql"}


app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutations))) #, mutation=Mutations