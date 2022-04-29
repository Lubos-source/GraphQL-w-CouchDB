from graphene import ObjectType, InputObjectType, Mutation, String, Int, Field
from conect import find_first, del_documents, update_user, insert_pymodel, insert_document, print_all, create_database, conectToCouch


class User(ObjectType):
    name=TextField()
    age=IntegerField()
    added=DateTimeField(default=datetime.now)

class UserInput(InputObjectType):
    #name = String(required=True)
    name=TextField()
    age=IntegerField()


class UserCreate(Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = Field(User)

    def mutate(root, info, user_data=None):
        loop.run_until_complete(insert_pymodel(user_data))
        print("Created")
        user = User(
            name=user_data.name,
            age=user_data.age
        )
        return UserCreate(user=user)

class UserUpdate(Mutation):
    class Arguments:
        user_data = UserInput(required=True)
        new_data = UserInput(required=True)

    user = Field(User)

    def mutate(root, info, user_data=None, new_data=None):
        loop.run_until_complete(do_update(user_data, new_data))
        print("Updated")
        user = User(
            name=new_data.name,
            group=new_data.group
        )
        return UserUpdate(user=user)

class UserDelete(Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = Field(User)

    def mutate(root, info, user_data=None):
        loop.run_until_complete(do_delete_many(user_data))
        print("Deleted")
        user = User(
            name=user_data.name,
            group=user_data.group
        )
        return UserDelete(user=user)
