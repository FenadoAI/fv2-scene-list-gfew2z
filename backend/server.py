from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class Todo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(BaseModel):
    text: str

class TodoUpdate(BaseModel):
    text: str = None
    completed: bool = None

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Todo endpoints
@api_router.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    todo_dict = todo.dict()
    todo_obj = Todo(**todo_dict)
    await db.todos.insert_one(todo_obj.dict())
    return todo_obj

@api_router.get("/todos", response_model=List[Todo])
async def get_todos():
    todos = await db.todos.find().sort("created_at", -1).to_list(1000)
    return [Todo(**todo) for todo in todos]

@api_router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    update_data = {k: v for k, v in todo_update.dict().items() if v is not None}
    await db.todos.update_one({"id": todo_id}, {"$set": update_data})
    updated_todo = await db.todos.find_one({"id": todo_id})
    if updated_todo:
        return Todo(**updated_todo)
    return None

@api_router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    result = await db.todos.delete_one({"id": todo_id})
    return {"deleted": result.deleted_count > 0}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
