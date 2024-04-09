"""main.py MODULE DOCSTRING
This is a simple FastAPI api to implement in a Kubernetes environment
"""
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine

# pylint: disable=C0115
# pylint: disable=C0116

# creating a FastAPI server
server = FastAPI(title='User API')

# creating a connection to the database
MYSQL_URL = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
DATABASE_NAME = 'Main'

# recreating the URL connection
connection_url = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_URL}/{DATABASE_NAME}'

# creating the connection
mysql_engine = create_engine(connection_url)


# creating a User class

class User(BaseModel): 
    user_id: int = 0
    username: str = 'daniel'
    email: str = 'daniel@datascientest.com'


@server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1


@server.get('/users')
async def get_users():
    with mysql_engine.connect() as connection:
        results = connection.execute('SELECT * FROM Users;')

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]
    return results


@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    with mysql_engine.connect() as connection:
        results = connection.execute(
            f'SELECT * FROM Users WHERE Users.id = {user_id};'
        )

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail='Unknown User ID')
    else:
        return results[0]
