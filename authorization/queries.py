import strawberry
from strawberry.django import auth
from strawberry.types import Info

from .types import User


async def resolve_whoami(root, info: Info) -> User | None:
    user = await info.context.request.auser()
    if user.is_anonymous:
        return None
    return user


@strawberry.type
class Query:
    whoami: User | None = strawberry.field(resolver=resolve_whoami)


@strawberry.type
class Mutation:
    login: User = auth.login()
    logout: bool = auth.logout()
