#!/usr/bin/env python
# coding: utf-8
import os

from dotenv import load_dotenv
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig

from .connection import Connection
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import mariadb
from .models import User, json_to_schema
from .utils import compare_items, make_update_statement
import logging

load_dotenv(f".env")

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"description": "Users router not found"}})


def get_conf():
    return ConnectionConfig(
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_FROM=os.getenv('MAIL_FROM'),
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_FROM_NAME="Pirogov AI Notifier",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True
    )


def get_body(user_name: str):
    body = ""
    with open("./routers/email.html") as f:
        body = f.read()
    body = body.replace("{name}", user_name)
    return body


async def send_message(user_name: str, user_email: str):
    conf = get_conf()
    body = get_body(user_name)
    message = MessageSchema(
        subject="Уведомление о завершении обучения",
        recipients=[user_email],
        body=body,
        subtype='html',
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


@router.post("/authorize")
def authorize(user: User):
    get_response = get_user(user.id)
    if get_response.status_code == status.HTTP_200_OK:
        update_response = update_user(user.id, user)
        if update_response.status_code == status.HTTP_200_OK:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"id": user.id})
        else:
            return update_response
    else:
        create_response = add_user(user)
        if create_response.status_code == status.HTTP_201_CREATED:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"id": user.id})
        else:
            return create_response


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    try:
        cursor.execute("insert into users(id, name, email) values (?, ?, ?)", (user.id, user.name, user.email))
        connection.commit()
        logging.info(f"User with body = {str(user)} has been created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": user.id})
    except mariadb.Error as e:
        logging.error(f"Could not create user with body: {str(user)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create user with body: {str(user)}")


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
                users.append(User(id=row[0], name=row[1], email=row[2]))
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
        user = User(id=user_raw[0][0], name=user_raw[0][1], email=user_raw[0][2])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(user))
    except mariadb.Error as e:
        logging.error(f"Could not get user with id = {user_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get user with id = {user_id}")


@router.put("/{user_id}")
def update_user(user_id: int, user: User):
    get_response = get_user(user_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_user = json_to_schema(get_response.body, User)
        user = User(id=user.id, name=user.name, email=user.email)
        updates = compare_items(old_user, user)
        statement, inserts = make_update_statement([user_id], "users", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
                logging.info(f"User with id = {user_id} has been updated successfully")
                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content=f"User with id = {user_id} has been updated successfully")
            except mariadb.Error as e:
                logging.error(f"Could not update user with body: {str(user)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update user with body: {str(user)}")
        else:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=f"User with id = {user_id} already has body: {str(user)}")
    else:
        return get_response


@router.post("/emails/{user_id}", status_code=status.HTTP_200_OK)
async def send_email(user_id: int):
    get_response = get_user(user_id)
    if get_response.status_code == 200:
        user = json_to_schema(get_response.body, User)
        name = user.name
        email = user.email
        try:
            await send_message(name, email)
        except mariadb.Error:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Could not send message for user with id: {user_id}")
    elif get_response.status_code == 404:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=f"Could not send email because user with id = {user_id} not found")
    else:
        return get_response
