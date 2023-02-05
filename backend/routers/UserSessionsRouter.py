#!/usr/bin/env python
# coding: utf-8
import os
import pathlib
import shutil

import mariadb
import patoolib
from fastapi import APIRouter, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import UserSession, UserSessionSummary, json_to_schema, HyperParams
from .utils import make_update_statement, compare_items, get_created_id
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
        entity_id = get_created_id(cursor, "user_session")[0][0]
        logging.info(f"User session with body = {str(user_session_body)} has been created successfully")
        return {"id": entity_id}
    except mariadb.Error as e:
        logging.error(f"Could not create user session with body: {str(user_session_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create user session with body: {str(user_session_body)}")


@router.delete("/{session_id:int}", status_code=status.HTTP_200_OK)
def delete_session(session_id: int):
    try:
        cursor.execute("delete from user_session where id = ?", (session_id,))
        logging.info(f"User session with id = {str(session_id)} has been deleted successfully")
    except mariadb.Error as e:
        logging.error(f"Could not delete user session with id = {str(session_id)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete user session with id = {str(session_id)}")


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
    except mariadb.Error as e:
        logging.error(f"Could not get sessions. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get sessions")


@router.get("/{session_id:int}", status_code=status.HTTP_200_OK)
def get_session(session_id: int):
    try:
        cursor.execute("select * from user_session where id = ?", (session_id,))
        session_raw = cursor.fetchall()
        if len(session_raw) == 0:
            logging.warning(f"User session with id = {session_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"User session with id = {session_id} not found")
        user_session = UserSession(id=session_raw[0][0], dataset_path=session_raw[0][1],
                                   data_markup_path=session_raw[0][2], user_id=session_raw[0][3])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(user_session))
    except mariadb.Error as e:
        logging.error(f"Could not get session with id = {session_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get session with id = {session_id}")


@router.put("/{session_id:int}", status_code=status.HTTP_200_OK)
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
                logging.info(f"User session with id = {session_id} has been updated successfully")
            except mariadb.Error as e:
                logging.error(f"Could not update session with body: {str(session)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update session with body: {str(session)}")
    else:
        return get_response


@router.post("/{session_id:int}/learn", status_code=status.HTTP_200_OK)
def launch_learning(session_id: int, hyperparams: HyperParams):
    try:
        get_response = get_session(session_id)
        if get_response.status_code == status.HTTP_200_OK:
            session = json_to_schema(get_response.body, UserSession)
            dataset_path = session.dataset_path
            markup_path = session.data_markup_path
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=f"Learning for session = {session_id} has been completed successfully")
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Could not start learning for session = {session_id}. "
                                        f"Cause: {get_response.body}")
    except Exception as e:
        logging.error(f"Could not start learning for session = {session_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=f"Could not start learning for session = {session_id}")


@router.post("/{session_id:int}/upload_dataset", status_code=status.HTTP_200_OK)
def upload_dataset(session_id: int, file: UploadFile = File(...)):
    try:
        if (pathlib.Path(file.filename).suffix == '.rar') or (pathlib.Path(file.filename).suffix == '.zip'):
            path_to_dir = f'{os.getcwd()}./dataset./{session_id}'
            is_exist = os.path.exists(path_to_dir)
            if not is_exist:
                os.makedirs(path_to_dir)
            with open(f'{file.filename}', "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            patoolib.extract_archive(archive=file.filename, outdir=path_to_dir)
            os.remove(file.filename)
            get_response = get_session(session_id)
            if get_response.status_code == status.HTTP_200_OK:
                body = json_to_schema(get_response.body, UserSession)
                update = UserSessionSummary(dataset_path=path_to_dir,
                                            data_markup_path=body.data_markup_path,
                                            user_id=body.user_id)
                return update_session(session_id, update)
            else:
                logging.error("Could not upload dataset file")
                return get_response
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content="Wrong file extension")
    except Exception as e:
        logging.error(f"Could not upload dataset file. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not upload dataset file")


@router.post("/{session_id:int}/upload_markup", status_code=status.HTTP_200_OK)
def upload_markup(session_id: int, file: UploadFile = File(...)):
    try:
        if pathlib.Path(file.filename).suffix == '.PirogovJSON':
            path_to_markup = f'{os.getcwd()}./markup./{session_id}_markup.json'
            with open(f'{file.filename}', "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            shutil.move(file.filename, path_to_markup)
            get_response = get_session(session_id)
            if get_response.status_code == status.HTTP_200_OK:
                body = json_to_schema(get_response.body, UserSession)
                update = UserSessionSummary(dataset_path=body.dataset_path,
                                            data_markup_path=path_to_markup,
                                            user_id=body.user_id)
                return update_session(session_id, update)
            else:
                logging.error("Could not upload markup file")
                return get_response
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content="Wrong file extension")
    except Exception as e:
        logging.error(f"Could not upload markup file. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not upload markup file")
