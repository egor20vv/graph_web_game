import uvicorn

from pydantic import BaseModel

from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend

from fastapi_sessions.session_verifier import SessionVerifier
from fastapi import HTTPException

from uuid import uuid4
from fastapi import FastAPI, Response
from fastapi import Depends


# --------------
#  Session Data
# --------------

class SessionData(BaseModel):
    username: str


# ------------------
#  Session Frontend
# ------------------

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name='my_cookie',
    identifier='general_verifier',
    auto_error=True,
    secret_key='DONOTUSE',
    cookie_params=cookie_params
)


# -----------------
#  Session Backend
# -----------------

backend = InMemoryBackend[UUID, SessionData]()


# ------------------
#  Session Verifier
# ------------------

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


# ---------------
#  Session Route
# ---------------

app = FastAPI()


@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"


if __name__ == '__main__':
    uvicorn.run("try_to_use_sessions:app", port=5000, reload=True, access_log=False)
