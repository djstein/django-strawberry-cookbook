import strawberry
from django.contrib.auth import get_user_model
from strawberry import auto

UserModel = get_user_model()


@strawberry.django.type(UserModel)
class User:
    id: auto
    email: auto
