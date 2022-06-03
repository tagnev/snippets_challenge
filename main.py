from fastapi import FastAPI,  Request, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta


class Snippet(BaseModel):
    name: str
    expires_in: int
    snippet: str

  
class SnippetURL(Snippet):
  url: Optional[str] = None
  expires_at: Optional[datetime] = None



app = FastAPI()

recipe_output = []

@app.get("/{snippet}")
async def get_snippet(snippet):
    # print(recipe_output)
    for val in recipe_output:
      if val['name'] == snippet.lower():
        if datetime.now() < val['expires_at']:
          # print(val['expires_at'], ' ', datetime.now())
          return val
        else:
          raise HTTPException(status_code=404, detail="Snippet has been expired")

    raise HTTPException(status_code=404, detail="Snippet not found")
    # return recipe


@app.post("/snippet" ,status_code=201)
async def create_snipet(snippet: Snippet, request: Request):
    url = f'{request.url}/{snippet.name}'
    expires_at = datetime.now() + timedelta(seconds=snippet.expires_in)
    expires_at += timedelta(seconds=3)
    output = {
        "url" : url,
        "name": snippet.name,
        "expires_at": expires_at,
        "snippet": snippet.snippet
    }
    recipe_output.append(output)
    return output 
  
uvicorn.run(app,host="0.0.0.0",port="8080")