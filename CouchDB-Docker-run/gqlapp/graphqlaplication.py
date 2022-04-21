from graphene import ObjectType, String, Int, Field, ID, List, Date, DateTime, Mutation, Boolean
from graphene import Schema as GSchema

from starlette.graphql import GraphQLApp
import graphene

#from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel

from contextlib import contextmanager


def attachGraphQL(app, sessionFunc, bindPoint='/gql'):
    """Attaches a Swagger endpoint to a FastAPI

    Parameters
    ----------
    app: FastAPI
        app to bind to
    prepareSession: lambda : session
        callable which returns a db session
    """
    assert callable(sessionFunc), "sessionFunc must be a function creating a session"

    session_scope = contextmanager(sessionFunc)

    def extractSession(info):
        return info.context.get('session')

    class Query(ObjectType):

        #user = Field(User, id=ID(required=True))
        #group = Field(Group, id=ID(required=False, default_value=None), name=String(required=False, default_value=None))


        """def resolve_user(root, info, id):
            #return {'name': info.context.get('session'), 'id': id}
            #return {'name': info.context['session'], 'id': id}
            session = extractSession(info)
            return session.query(UserModel).get(id)
        
        def resolve_group(root, info, id=None, name=None):
            
            session = extractSession(info)
            if id is None:
                return session.query(GroupModel).filter(GroupModel.name == name).first()
            else:
                return session.query(GroupModel).get(id)"""

    """class Mutations(ObjectType):
        create_user = CreateUser.Field()
        update_user = UpdateUser.Field()"""


    class localSchema(graphene.Schema):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

        def execute(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return super().execute(*args, **newkwargs)

        async def execute_async(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return await super().execute_async(*args, **newkwargs)


    #graphql_app = GraphQLApp(schema=localSchema(query=Query, mutation=Mutations))
    graphql_app = GraphQLApp(schema=localSchema(query=Query))
    
    #app.add_route('/gql', graphql_app)
    app.add_route(bindPoint, graphql_app)