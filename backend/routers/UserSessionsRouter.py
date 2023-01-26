#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import UserSession, UserSessionSummary, json_to_schema
from .utils import make_update_statement, compare_items
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/user-sessions",
                   tags=["user-sessions"],
                   responses={404: {"description": "User session router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_session(user_session_body: UserSessionSummary):
    try:
        cursor.execute("insert into user_session(dataset_path, data_markup_path, user_id) values (?, ?, ?)",
                       (user_session_body.dataset_path, user_session_body.data_markup_path,
                        user_session_body.user_id))
        connection.commit()
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create user session with body: {str(user_session_body)}")


@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
def delete_session(session_id: int):
    try:
        cursor.execute("delete from user_session where id = ?", (session_id,))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete user_session with id = {str(session_id)}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_sessions():
    try:
        cursor.execute("select * from user_session")
        sessions = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                sessions.append(
                    UserSession(id=row[0], dataset_path=row[1], data_markup_path=row[2], user_id=row[3]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(sessions))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get sessions")


@router.get("/{session_id}", status_code=status.HTTP_200_OK)
def get_session(session_id: int):
    try:
        cursor.execute("select * from user_session where id = ?", (session_id,))
        session_raw = cursor.fetchall()
        if len(session_raw) == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Session with id = {session_id} not found")
        optimizer = UserSession(id=session_raw[0][0], dataset_path=session_raw[0][1],
                                data_markup_path=session_raw[0][2], user_id=session_raw[0][3])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(optimizer))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get session with id = {session_id}")


@router.put("/{session_id}", status_code=status.HTTP_200_OK)
def update_session(session_id: int, session: UserSessionSummary):
    get_response = get_session(session_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_session = json_to_schema(get_response.body, UserSession)
        session = UserSession(id=session_id, dataset_path=session.dataset_path,
                              data_markup_path=session.data_markup_path, user_id=session.user_id)
        updates = compare_items(old_session, session)
        statement, inserts = make_update_statement([session_id], "user_session", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update session with body: {str(session)}")
    else:
        return get_response


@router.post("/{session_id}/learn")
def launch_learning(session_id: int, parameters: dict):
    get_response = get_session(session_id)
    if get_response.status_code == status.HTTP_200_OK:
        session = json_to_schema(get_response.body, UserSession)
        dataset_path = session.dataset_path
        markup_path = session.data_markup_path
