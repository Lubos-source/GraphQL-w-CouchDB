from starlette.graphql import GraphQLApp

from dbInit import get_bucket

from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel

import dbInit

from fastapi import FastAPI
import graphqlapp
#import svgapp

#from fastapi.middleware.cors import CORSMiddleware


def buildApp():
    Session = get_bucket()
    
    def prepareSession():#Session=Session): # default parameters are not allowed here
        """generator for creating db session encapsulated with try/except block and followed session.commit() / session.rollback()

        Returns
        -------
        generator
            contains just one item which is instance of Session (SQLAlchemy)
        """
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close() 
            
    app = FastAPI()

    #origins = ["http://localhost:3000", "http://localhost:50055",]
    #app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
    
    graphqlapp.attachGraphQL(app, prepareSession)
    #svgapp.attachSVGApp(app)
    return app

dbInit.InitAndRandomize()
print('All initialization is done')
app = buildApp()
