from typing import Optional

import uvicorn

from fastapi import FastAPI, Response, status, Cookie
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.requests import Request

app = FastAPI()


@app.post("/create_session/{name}")
async def create_session(name: str, rr: Response):

    print(rr.__dict__)

    content = {"message": f"created session for {name}"}
    response = JSONResponse(content=content)
    response.set_cookie(key="name", value=name)
    return response


@app.get("/whoami")
async def whoami(request: Request, cookies: Optional[str] = Cookie(None)):
    value = request.cookies['name'] if 'name' in request.cookies else None
    return JSONResponse(content={'name': value}, status_code=status.HTTP_200_OK)


@app.post("/delete_session")
async def del_session(response: Response):
    response.delete_cookie('name')
    return "deleted session"


if __name__ == '__main__':
    uvicorn.run("try_to_use_cookies:app", port=5000, reload=True, access_log=False)