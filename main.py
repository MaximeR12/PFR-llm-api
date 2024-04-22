import ollama
from fastapi import FastAPI, Security, Response, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI()

valid_users = {
    "user1": "password1",
    "user2": "password2",
}

class Script(BaseModel):
    script: str

class Token(BaseModel):
    token: str

security = HTTPBearer()

def authenticate(token: str = Security(security)):
    if token not in valid_users.values():
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

@app.post("/script_analyse")
async def ollama_chat(script: Script, token: HTTPAuthorizationCredentials = Security(security)):
    if not authenticate(token.credentials):
        return Response(status_code=401, content="Unauthorized")
    output = ollama.chat(
      model='llama3:8b',
      messages=[{'role': 'user', 'content': """Context : You are a Data lineage assistant, you help a data steward by creating a csv file that lists all source/target relations between tables of a sql script.
      The csv file must follow this structure :
      source_schema, source_table, target_schema, target_table
      
      List all source/target relations between the different tables of this sql script:"""+ script.script +". The output you provide should only contain the csv content"
                  }])
    return output['message']['content']
