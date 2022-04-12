import os
import json
from functools import cache
###############################

from typing import Optional

from couchbase import LOCKMODE_WAIT
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster, PasswordAuthenticator

from fastapi import FastAPI
from pydantic import BaseModel

#################################

from DatabaseModel.sqlalchemyCore import initEngine, initSession, GetDeclarativeBase
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel
#from DatabaseModel import sqlalchemyCore #přístup do modulu přes tečku


USERPROFILE_DOC_TYPE = "userprofile"
@cache
def get_bucket():
    """
        bucket is a set of documents
        This function do :  Connect to a Couchbase cluster (+set defaults)
                            Authenticate in the cluster
                            Get a "Bucket" instance (+set defaults)
                            and return it ;)
    """
    cluster = Cluster(
        "couchbase://localhost:31111?fetch_mutation_tokens=1&operation_timeout=30&n1ql_timeout=300"
    )
    authenticator = PasswordAuthenticator("admin", "admin")
    cluster.authenticate(authenticator)
    bucket: Bucket = cluster.open_bucket("bucket_name", lockmode=LOCKMODE_WAIT)
    bucket.timeout = 30
    bucket.n1ql_timeout = 300
    return bucket



##### TVORBA MODELŮ - později samostatný soubor ? #####

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """
        This will have the data that is actually stored in the database
        Same atributes as User (thats why subclas of User ;) ) + some more atributes like password etc... secret ones ;)
    """
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str


def get_user(bucket: Bucket, username: str):
    """
        function do:    Take a username.
                        Generate a document ID from it.
                        Get the document with that ID.
                        Put the contents of the document in a UserInDB model.
    """
    doc_id = f"userprofile::{username}"
    """ Python variable "f-string::" : Any variable that is put inside of {} in an f-string will be expanded / injected in the string. """
    result = bucket.get(doc_id, quiet=True)
    if not result.value:
        return None
    user = UserInDB(**result.value)
    """ dictionary unpacking : 
        It will take the dict at result.value, and take each of its keys and values 
        and pass them as key-values to UserInDB as keyword arguments.
    """
    return user



#### FAST API - asi zase samostatny soubor ???? ####
# FastAPI specific code

#app = FastAPI()

def connectAllEndpoints(app):
    @app.get("/users/{username}", response_model=User)
    def read_user(username: str):
        bucket = get_bucket()
        user = get_user(bucket=bucket, username=username)
        return user