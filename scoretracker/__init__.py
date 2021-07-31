from strawberry import Schema
from strawberry.asgi import GraphQL

from .mutation import Mutation
from .query import Query

schema = Schema(query=Query, mutation=Mutation)
app = GraphQL(schema)
