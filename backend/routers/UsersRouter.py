#!/usr/bin/env python
# coding: utf-8

from .connection import Connection
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import mariadb
from .models import User, json_to_schema
from .utils import compare_items, make_update_statement, get_created_id
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"description": "Users router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(user_body: User):
    try:
        cursor.execute("insert into users(id) values (?)", (user_body.id,))
        connection.commit()
        entity_id = get_created_id(cursor, "users")[0][0]
        logging.info(f"User with body = {str(user_body)} has been created successfully")
        return {"id": entity_id}
    except mariadb.Error as e:
        logging.error(f"Could not create user with body: {str(user_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create user with body: {str(user_body)}")


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    try:
        cursor.execute("delete from users where id = ?", (user_id,))
        logging.info(f"User with id = {str(user_id)} has been deleted successfully")
    except mariadb.Error as e:
        logging.error(f"Could not delete user with id = {str(user_id)}. Error: {e}")
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
    except mariadb.Error as e:
        logging.error(f"Could not get users. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get users")


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    try:
        cursor.execute("select * from users where id = ?", (user_id,))
        user_raw = cursor.fetchall()
        if len(user_raw) == 0:
            logging.warning(f"User with id = {user_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"User with id = {user_id} not found")
        user = User(id=user_raw[0][0], )
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(user))
    except mariadb.Error as e:
        logging.error(f"Could not get user with id = {user_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get user with id = {user_id}")


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User):
    get_response = get_user(user_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_user = json_to_schema(get_response.body, User)
        user = User(id=user.id)
        updates = compare_items(old_user, user)
        statement, inserts = make_update_statement([user_id], "users", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
                logging.info(f"User with id = {user_id} has been updated successfully")
            except mariadb.Error as e:
                logging.error(f"Could not update user with body: {str(user)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update user with body: {str(user)}")
    else:
        return get_response
