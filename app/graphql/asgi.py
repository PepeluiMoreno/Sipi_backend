import os, uvicorn
from strawberry.asgi import GraphQL
from .schema import schema
from .context import GQLContext

def get_context():
    return GQLContext()

app = GraphQL(schema, graphiql=True, context_getter=lambda request: get_context())

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("GRAPHQL_HOST","0.0.0.0"), port=int(os.getenv("GRAPHQL_PORT","8040")))
