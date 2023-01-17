#!/usr/bin/env python
# coding: utf-8

from Connection import Connection
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mariadb

class UserSession(BaseModel):
    id: int
    dataset_path: str
    data_markup_path: str
    user_id: int

class UserSessionSummary(BaseModel):
    dataset_path: str
    data_markup_path: str
    user_id: int


def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response

router = APIRouter(prefix="/user-sessions",
                            tags=["user-sessions"],
                            responses={404: {"description": "User session router not found"}})

def compare_sessions(old_user_session, new_user_session):
    updates = []
    for old_pair, new_pair in zip(old_user_session, new_user_session):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates

def make_update_statement(user_session_id, updates):
    statement = "update user_session set "
    session_row = []
    inserts = []
    for pair in updates:
        session_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(user_session_id)
    statement += ", ".join(session_row) + " where id = ?"
    return statement, (*inserts, )

def init_router():
    response = connect()
    if response.status_code != 200:
        return response
    else:
        connection = response.body
        cursor = response.body.cursor()
        @router.post("/", status_code=status.HTTP_201_CREATED)
        def add_session(user_session_body: UserSessionSummary, response: Response):
            try:
                cursor.execute("insert into user_session(dataset_path, data_markup_path, user_id) values (?, ?, ?)",
                               (user_session_body.dataset_path, user_session_body.data_markup_path, user_session_body.user_id))
                connection.commit()
            except Exception  as e:
                response.body = f"Could not create user session with body: {str(user_session_body)}"
                response.status_code = status.HTTP_400_BAD_REQUEST


        @router.delete("/{session_id}", status_code=status.HTTP_200_OK)
        def delete_session(session_id: int, response: Response):
            try:
                cursor.execute("delete from user_session where id = ?", (session_id,))
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not delete user_session with id = {str(session_id)}"

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_sessions(response: Response):
            try:
                cursor.execute("select * from user_session")
                sessions = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        sessions.append(UserSession(id=row[0],dataset_path=row[1],data_markup_path=row[2],user_id=row[3]))
                return sessions
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = "Could not get sessions, error = {e}"
    
        @router.get("/{session_id}", status_code=status.HTTP_200_OK)
        def get_session(session_id: int, response: Response):
            try:
                cursor.execute("select * from user_session where id = ?", (session_id, ))
                session_raw = cursor.fetchall()
                if len(session_raw) == 0:
                    raise mariadb.Error(f"Session with id = {session_id} not found")
            except mariadb.Error as e:
                response.status_code = status.HTTP_404_NOT_FOUND
                response.body = f"Session with id = {session_id} not found"
            optimizer = UserSession(id=session_raw[0][0],dataset_path=session_raw[0][1],data_markup_path=session_raw[0][2],user_id=session_raw[0][3])
            return optimizer

        @router.put("/{session_id}", status_code=status.HTTP_200_OK)
        def update_session(session_id: int, session: UserSessionSummary, response: Response):
            old_session = get_session(session_id, response)
            session = UserSession(id=session_id, dataset_path=session.dataset_path,data_markup_path=session.data_markup_path,user_id=session.user_id)
            updates = compare_sessions(old_session, session)
            statement, inserts = make_update_statement(session_id, updates)
            if len(inserts) > 1:
                try:
                    cursor.execute(statement, inserts)
                    connection.commit()
                except mariadb.Error as e:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    response.body = f"Could not update session with body: {str(session)}"
init_router()
