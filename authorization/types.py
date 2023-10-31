import strawberry
from django.contrib.auth import get_user_model
from strawberry import auto

User = get_user_model()


@strawberry.django.type(User)
class User:
    id: auto
    email: auto
