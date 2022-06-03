from fastapi import FastAPI,  Request, HTTPException
import uvicorn
from pydantic import BaseModel
# from typing import Optional
from datetime import datetime, timedelta


class Snippet(BaseModel):
    name: str
    expires_in: int
    snippet: str
    # Below field for extension use case
    password: str

  
class SnippetEdit(BaseModel):
    password: str
    snippet: str



app = FastAPI(
    docs_url="/api/v1",
    openapi_url="/api/v1/openapi.json",
    title='Stellar Challenge API - Vengat',
    description='This API for Stellar Foundation Interview challenge',
     version="0.0.1",
     contact={
        "name": "Vengateswaran Arunachalam",
        "email": "tagnev.vengat@gmail.com",
    },
    )

# to store the snippet data
SNIPPET_MEMORY_OUTPUT = []

# GET request to get the particulat Snippet detail
@app.get("/snippets/{snippet}")
async def get_snippet(snippet):
    for val in SNIPPET_MEMORY_OUTPUT:
      if val['name'].lower() == snippet.lower():
        # validating the expiration before render to the users
        if datetime.now() < val['expires_at']:
          return val
        else:
          raise HTTPException(status_code=404, detail=f"{snippet} snippet has been expired")

    raise HTTPException(status_code=404, detail=f"{snippet} snippet doesnt exists")

# POST request to create the new snippet
@app.post("/snippets" ,status_code=201)
async def create_snipet(snippet: Snippet, request: Request):
    url = f'{request.url}/{snippet.name}'
    expires_at = datetime.now() + timedelta(seconds=snippet.expires_in)
    output = {
        "url" : url,
        "name": snippet.name,
        "expires_at": expires_at,
        "snippet": snippet.snippet,
        "password": snippet.password
    }
    # Adding the new snippet into Array memory for further processing
    SNIPPET_MEMORY_OUTPUT.append(output)
    return output 

@app.put("/snippets/{snippet}" ,status_code=200)
async def update_snippet(requestbody: SnippetEdit, snippet):
    # print(SNIPPET_MEMORY_OUTPUT)
    for ind,val in enumerate(SNIPPET_MEMORY_OUTPUT):
      # print(ind,val)
      # Check the snippet name exists in our memory or not
      if val['name'].lower() == snippet.lower():
        # Validate the password
        if requestbody.password == val['password']:
          updated_output = {
            "url" : val['url'],
            "name": val['name'],
            "expires_at": val['expires_at'],
            "snippet": requestbody.snippet,
            "password": requestbody.password
        }
          SNIPPET_MEMORY_OUTPUT.pop(ind)
          SNIPPET_MEMORY_OUTPUT.append(updated_output)
          return updated_output
        else:
          raise HTTPException(status_code=400, detail=f"Password doesnt match") 

      else:
         raise HTTPException(status_code=404, detail=f"{snippet} snippet doesnt exists") 
        
      
      

uvicorn.run(app,host="0.0.0.0",port="8080")