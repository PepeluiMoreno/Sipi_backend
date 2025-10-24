from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.graphql.context import get_context
from app.db.session import SessionLocal
from app.utils.config import ENV, ALLOWED_ORIGINS, GRAPHIQL_ENABLED

app = FastAPI(title='SIPI GraphQL API')
app.state.env = ENV

if ENV == 'production':
    app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS or [], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
else:
    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    try:
        response: Response = await call_next(request)
        request.state.db.commit()
        return response
    except Exception:
        request.state.db.rollback()
        raise
    finally:
        request.state.db.close()

graphql_app = GraphQLRouter(schema, context_getter=get_context, graphiql=GRAPHIQL_ENABLED)

@app.get('/health')
def health():
    return {'status': 'ok'}

app.include_router(graphql_app, prefix='/graphql')
