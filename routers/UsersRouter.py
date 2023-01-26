#!/usr/bin/env python
# coding: utf-8

from Connection import Connection
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import mariadb
from models import User, json_to_schema


def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"description": "Users router not found"}})


def compare_users(old_user, new_user):
    updates = []
    for old_pair, new_pair in zip(old_user, new_user):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates


def make_update_statement(user_id, updates):
    statement = "update users set "
    users_row = []
    inserts = []
    for pair in updates:
        users_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(user_id)
    statement += ", ".join(users_row) + " where id = ?"
    return statement, (*inserts,)


def init_router():
    response = connect()
    if response.status_code != 200:
        return response
    else:
        connection = response.body
        cursor = response.body.cursor()

        @router.post("/", status_code=status.HTTP_201_CREATED)
        def add_user(user_body: User):
            try:
                cursor.execute("insert into users(id) values (?)", (user_body.id,))
                connection.commit()
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not create user with body: {str(user_body)}")

        @router.delete("/{user_id}", status_code=status.HTTP_200_OK)
        def delete_user(user_id: int):
            try:
                cursor.execute("delete from users where id = ?", (user_id,))
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not delete user with id = {str(user_id)}")

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_users():
            try:
                cursor.execute("select * from users")
                users = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        users.append(User(id=row[0]))
                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content=jsonable_encoder(users))
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content="Could not get users")

        @router.get("/{user_id}", status_code=status.HTTP_200_OK)
        def get_user(user_id: int):
            try:
                cursor.execute("select * from users where id = ?", (user_id,))
                user_raw = cursor.fetchall()
                if len(user_raw) == 0:
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                        content=f"User with id = {user_id} not found")
                user = User(id=user_raw[0][0], )
                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content=jsonable_encoder(user))
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not get user with id = {user_id}")

        @router.put("/{user_id}", status_code=status.HTTP_200_OK)
        def update_user(user_id: int, user: User):
            get_response = get_user(user_id)
            if get_response.status_code == status.HTTP_200_OK:
                old_user = json_to_schema(get_response.body, User)
                user = User(id=user.id)
                updates = compare_users(old_user, user)
                statement, inserts = make_update_statement(user_id, updates)
                if len(inserts) > 1:
                    try:
                        cursor.execute(statement, inserts)
                        connection.commit()
                    except mariadb.Error:
                        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                            content=f"Could not update user with body: {str(user)}")
            else:
                return get_response


init_router()
