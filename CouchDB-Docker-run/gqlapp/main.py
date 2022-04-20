
###########################################################x
##########################################################
#############################################################

#import conect
from conect import conectToCouch

#from starlette.graphql import GraphQLApp
from fastapi import FastAPI
import graphqlaplication as gqlapp

def buildApp():
    Session = conectToCouch()
    
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
    
    gqlapp.attachGraphQL(app, prepareSession)
    #svgapp.attachSVGApp(app)
    return app

#dbInit.InitAndRandomize()
print('All initialization is done')
app = buildApp()