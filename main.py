import ollama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Script(BaseModel):
    script: str

@app.post("/script_analyse")
async def ollama_chat(script : Script):
  output = ollama.chat(
    model='llama3:8b',
    messages=[{'role': 'user', 'content': """Context : You are a Data lineage assistant, you help a data steward by creating a csv file that lists all source/target relations between tables of a sql script.
    The csv file must follow this structure :
    source_schema, source_table, target_schema, target_table
    
    List all source/target relations between the different tables of this sql script:"""+ script.script +". The output you provide should only contain the csv content"
                }])
  return output['message']['content']
