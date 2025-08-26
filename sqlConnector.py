import pwd
import sqlite3
import datetime
import pydantic

sqlConn = sqlite3.connect('./SQL/user.db')
sqlCursor = sqlConn.cursor()

# sqlCursor.execute("""create table users(dateOfCreation date NOT NULL ,
# userName varchar(64) NOT NULL
# androidID varchar(32) UNIQUE NOT NULL,
# email varchar(320) PRIMARY KEY UNIQUE NOT NULL,
# pwd varchar(255) NOT NULL ,
# clgName varchar(255) NOT NULL )""")

def userAdd(androidID:str,email: pydantic.EmailStr,pwd: str,clgName: str,userName:str):
    dateOfCreation = datetime.date.today()
    sqlCursor.execute(f"insert into users(dateOfCreation,userName:str,androidID,email,pwd,clgName) values({dateOfCreation},{userName},{androidID},{email},{pwd},{clgName});")
    sqlConn.commit()

def userAuth(androidID:str,pwd:str,userName:str):
    sqlCursor.execute(f"select * from users where androidID={androidID} and (userName={userName} or email = {userName}) and pwd={pwd};")
    x = sqlCursor.fetchall()
    if not x:
        return False
    else:
        return True

def userDelete(androidID:str,email: pydantic.EmailStr,userName:str,pwd: str):
    sqlCursor.execute(f"select * from users where email={email} and userName={userName};")
    [values] = sqlCursor.fetchall()
    if androidID == values[1]:
        sqlCursor.execute(f"delete from users where androidID={androidID} and email={email} and userName={userName} and pwd={pwd};")
        sqlConn.commit()
        return True
    else:
        return False

