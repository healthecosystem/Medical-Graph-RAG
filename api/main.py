# Python Imports
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import os
from dotenv import load_dotenv
from camel.storages import Neo4jGraph
from dataloader import load_high
from summerize import process_chunks
from retrieve import seq_ret
from utils import get_response
from creat_graph import creat_metagraph

from fastapi import FastAPI  # , Path, HTTPException, Body, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware


from api.logger import get_logger_by_name
from fastapi import APIRouter
from utils import str_uuid, link_context, merge_similar_nodes, get_response

logger = get_logger_by_name("Hivata | Rare diseases | Knowledge Graph")

try:
    url = os.getenv("NEO4J_URI")
    if not url:
        raise ValueError("NEO4J_URI is not set.")
except ValueError as e:
    raise SystemExit(f"Error: {e}")

# Check NEO4J_PASSWORD
try:
    password = os.getenv("NEO4J_PASSWORD")
    if not password:
        raise ValueError("NEO4J_PASSWORD is not set.")
except ValueError as e:
    raise SystemExit(f"Error: {e}")

# Set Neo4j instance
n4j = Neo4jGraph(
    url=url,
    username="neo4j",  # Default username
    password=password,  # Replace 'yourpassword' with your actual password
)
LOCAL_DIR = "/datasets/mimiciii"

files = [
    file
    for file in os.listdir(LOCAL_DIR)
    if os.path.isfile(os.path.join(LOCAL_DIR, file))
]

# Read and print the contents of each file
for file_name in files:
    file_path = os.path.join(LOCAL_DIR, file_name)
    content = load_high(file_path)
    gid = str_uuid()
    n4j = creat_metagraph(args, content, gid, n4j)

    # if args.trinity:
    link_context(n4j, args.trinity_gid1)
# if args.crossgraphmerge:
merge_similar_nodes(n4j, None)


class BodySizeLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body_size = len(await request.body())
        if body_size > 512 * 1024 * 1024:  # 100 MB
            return JSONResponse({"detail": "Request body too large"}, status_code=413)
        response = await call_next(request)
        return response


load_dotenv()

example_project_id = str(uuid4())
router = APIRouter(prefix="/api/v1")
app = FastAPI(
    title="Hivata Knowledge Graph",
    description="""Knowledge Graph service on rare diseases for LLM retrieval""",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def get_application_health():
    api_message = "Up and running!"
    return {
        "message": api_message,
    }


# class syntax
@router.get("/knowledge")
async def get_knowledge(question: str):
    print("question", question)
    question = load_high("./prompt.txt")
    sum = process_chunks(question)
    gid = seq_ret(n4j, sum)
    response = get_response(n4j, gid, question)
    print(response)

    response = {"answer": response}
    return JSONResponse(content=response)


app.include_router(router)
app.add_middleware(BodySizeLimiterMiddleware)
