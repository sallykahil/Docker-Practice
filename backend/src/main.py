from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID,uuid4
from pydantic import Field
MONGODB_CONNECTION_STRING= os.getenv("MONGO_URI")
client= AsyncIOMotorClient(MONGODB_CONNECTION_STRING,
                           uuidRepresentation="standard")

database= client.tododb
todos= database.todos
app= FastAPI()
# Enable CORS middleware since without this it will blocked since javascript running in the browser enforces CORS policy and access hosst 80 and we are running backend on 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#mongo use _id as primary key so we need to set alias
class TodoItem(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    content: str

class TodoCreate(BaseModel):
    content: str

 
 

@app.post("/todos",response_model=TodoItem)
async def create_todo(todo: TodoCreate):
    new_todo = TodoItem(content=todo.content)
    await todos.insert_one(new_todo.dict(by_alias=True))    
    #todos.append(new_todo)
    #id_counter+=1
    return new_todo

@app.get("/todos",response_model=list[TodoItem])
async def get_todos():
    return await todos.find().to_list(length=None)
   # return todos    

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id:UUID):
     delete_result=await todos.delete_one({"_id":todo_id})
     if delete_result.deleted_count==0:
         raise HTTPException(status_code=404,detail="Todo not found")
     return {"message":"Todo deleted successfully"}
        
     