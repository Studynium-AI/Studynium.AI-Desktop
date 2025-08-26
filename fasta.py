import fastapi
import pydantic
import datetime
import main
import sqlConnector
from cryptography.fernet import Fernet as Cfr
app = fastapi.FastAPI()


class requestFormat(pydantic.BaseModel):
    # credits: int  #to be removed later after implementing storage in csv
    # androidID: str
    query: str
    # accountID: str
    model: int


class createUserRequest(pydantic.BaseModel):
    date: datetime.datetime
    userName: str
    androidID: str
    email: pydantic.EmailStr
    pwd: str
    clgName: str

class authUserRequest(pydantic.BaseModel):
    userName: str
    androidID: str
    pwd: str

class answerFormat(pydantic.BaseModel):
    status: str
    answer: str

class delUserRequest(pydantic.BaseModel):
    userName: str
    email: pydantic.EmailStr
    androidID: str
    pwd: str

#path definitions

USER = "/user"
REQUEST_HANDLER = "/request"


@app.post(REQUEST_HANDLER)
def serve(request: requestFormat):
    x = main.main(prompt=request.query, action="1", modelInfo=request.model)
    return x


@app.post(USER)
def createUser(request: createUserRequest):
    sqlConnector.userAdd(androidID=request.androidID,email=request.email,pwd=request.pwd,clgName=request.clgName,userName=request.userName)
    return "User created successfully"

@app.get(USER)
def authUser(request: authUserRequest):
    x = sqlConnector.userAuth(androidID=request.androidID,userName=request.userName,pwd=request.pwd)
    if x:
        return {"status": "success"}
    else:
        return {"status": "Invalid UserName or Password"}

@app.delete(USER)
def deleteUser(request: delUserRequest):
    x = sqlConnector.userDelete(androidID=request.androidID, email=request.email, userName=request.userName, pwd=request.pwd)
    if x:
        return "User deleted successfully"
    else:
        return "User not on the same device"