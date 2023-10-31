from strawberry import Schema
from strawberry.tools import merge_types
from strawberry_django.optimizer import DjangoOptimizerExtension

from authorization.queries import Mutation as AuthMutations
from authorization.queries import Query as AuthQueries

queries = (AuthQueries,)
mutations = (AuthMutations,)
Query = merge_types("Query", queries)
Mutations = merge_types("Mutation", mutations)

schema = Schema(
    query=Query,
    mutation=Mutations,
    subscription=None,
    extensions=[DjangoOptimizerExtension],
)
