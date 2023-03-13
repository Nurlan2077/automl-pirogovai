#!/usr/bin/env python
# coding: utf-8
import asyncio
import logging
import os
import pathlib
import shutil
import sys
import traceback
import zipfile
from io import BytesIO

import mariadb
import rarfile
from fastapi import APIRouter, status, UploadFile, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from starlette.websockets import WebSocketDisconnect

from .LossFunctionsRouter import get_loss_function_by_name
from .MetricsRouter import get_metric_by_name
from .ModelMetricsRouter import add_model_metric
from .ModelsRouter import add_model
from .OptimizersRouter import get_optimizer_by_name
from .connection import Connection
from .models import UserSession, UserSessionSummary, json_to_schema, HyperParams, Optimizer, LossFunction, ModelSummary, \
    ModelMetric, Metric
from .utils import make_update_statement, compare_items, get_created_id, get_id
from .UsersRouter import send_email

sys.path.append("/app/ml")
from learning_utils import learn_models

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
        cursor.execute(
            "insert into user_session(dataset_path, data_markup_path, model_path, user_id) values (?, ?, ?, ?)",
            (user_session_body.dataset_path, user_session_body.data_markup_path,
             user_session_body.model_path, user_session_body.user_id))
        connection.commit()
        entity_id = get_created_id(cursor, "user_session")[0][0]
        logging.info(f"User session with body = {str(user_session_body)} has been created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": entity_id})
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
                    UserSession(id=row[0], dataset_path=row[1], data_markup_path=row[2], user_id=row[3],
                                model_path=row[4]))
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
        logging.info(session_raw[0])
        user_session = UserSession(id=session_raw[0][0], dataset_path=session_raw[0][1],
                                   data_markup_path=session_raw[0][2], user_id=session_raw[0][3],
                                   model_path=session_raw[0][4])
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
                              data_markup_path=session.data_markup_path, model_path=session.model_path,
                              user_id=session.user_id)
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


@router.get("/{session_id:int}/send-archive")
def send_archive(session_id: int):
    get_response = get_session(session_id)
    if get_response.status_code == status.HTTP_200_OK:
        session = json_to_schema(get_response.body, UserSession)
        model_path = session.model_path
        file_list = [model_path]
        logging.info(f'{file_list}')
        zip_io = BytesIO()
        with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
            for file in file_list:
                temp_zip.write(file)
        return StreamingResponse(
            iter([zip_io.getvalue()]),
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename=models-archive.zip"}
        )


def get_model_optimizer(model_name: str):
    first_underscore = model_name.find("_")
    optimizer_name = model_name[:first_underscore]
    optimizer_response = get_optimizer_by_name(optimizer_name)
    if optimizer_response.status_code == status.HTTP_200_OK:
        optimizer_id = json_to_schema(optimizer_response.body, Optimizer).id
    else:
        optimizer_id = None
    return optimizer_id


def get_model_loss_function(model_name: str):
    first_underscore = model_name.find("_")
    loss_function_name = model_name[first_underscore + 1:]
    loss_function_response = get_loss_function_by_name(loss_function_name)
    if loss_function_response.status_code == status.HTTP_200_OK:
        loss_function_id = json_to_schema(loss_function_response.body, LossFunction).id
    else:
        loss_function_id = None
    return loss_function_id


def save_model_to_db(model_name: str, session_id: int, epochs: int):
    model_summary = ModelSummary(session_id=session_id,
                                 name=model_name,
                                 features_cnn_id=1,
                                 optimizer_id=get_model_optimizer(model_name),
                                 loss_function_id=get_model_loss_function(model_name),
                                 augmentation=1,
                                 learning_speed=1,
                                 epoch_count=epochs)
    model_response = add_model(model_summary)
    if model_response.status_code == status.HTTP_201_CREATED:
        return get_id(model_response.body)
    else:
        model_id = None
    return model_id


def get_metric_id(metric_name: str):
    metric_response = get_metric_by_name(metric_name)
    logging.info(f"{metric_response}")
    logging.info(f"{metric_response.body}")
    if metric_response.status_code == status.HTTP_200_OK:
        metric_id = json_to_schema(metric_response.body, Metric).id
    else:
        metric_id = None
    return metric_id


def save_model_metrics_to_db(model_id: int, metrics: dict):
    if model_id is None:
        logging.error(f"Could not save model metrics with null model_id")
    else:
        for metric_name, metric_value in metrics.items():
            metric_id = get_metric_id(metric_name)
            if metric_id is None:
                logging.error(f"Could not save model metric with metric name = {metric_name}")
                continue
            summary = ModelMetric(model_id=model_id,
                                  metric_id=metric_id,
                                  metric_value=metric_value)
            add_model_metric(summary)


def get_model_name(path_to_model: str):
    last_slash = path_to_model.rfind("/")
    dot = path_to_model.find(".")
    return path_to_model[last_slash + 1:dot]


@router.websocket("/{session_id:int}/progress")
async def progress_socket(session_id: int, websocket: WebSocket):
    try:
        get_response = get_session(session_id)
        if get_response.status_code == status.HTTP_200_OK:
            session: UserSession = json_to_schema(get_response.body, UserSession)
            dataset_path = session.dataset_path
            data_markup_path = session.data_markup_path
            model_path = session.model_path
            global hyperparams
            try:
                await websocket.accept()
                updated_model_path, metrics, epochs = await learn_models(websocket, dataset_path, model_path,
                                                                         hyperparams)
                session_summary = UserSessionSummary(dataset_path=dataset_path,
                                                     data_markup_path=data_markup_path,
                                                     model_path=updated_model_path,
                                                     user_id=session.user_id)
                update_session(session_id, session_summary)
                model_id = save_model_to_db(get_model_name(updated_model_path), session_id, epochs)
                save_model_metrics_to_db(model_id, metrics)
                await asyncio.sleep(1)
                await websocket.send_text(f"model id: {model_id}")
                await asyncio.sleep(1)
                await websocket.send_text("Processing completed.")
                await websocket.close()
                await send_email(session.user_id)
            except WebSocketDisconnect as e:
                logging.error(f"{e}")
    except Exception as e:
        logging.error(f"Could not make learning for session = {session_id}. Error: {e}")


hyperparams: HyperParams


@router.post("/{session_id:int}/learn", status_code=status.HTTP_200_OK)
def launch_learning(session_id: int, hyperparams_: HyperParams):
    try:
        get_response = get_session(session_id)
        if get_response.status_code == status.HTTP_200_OK:
            global hyperparams
            hyperparams = hyperparams_
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=f"Successfully received hyperparameters for session = {session_id}")
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Could not receive hyperparameters for session = {session_id}. "
                                        f"Cause: {get_response.body}")
    except Exception as e:
        logging.error(f"Could not receive hyperparameters for session = {session_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=f"Could not receive hyperparameters for session = {session_id}")


def make_model_folder(session_id: int):
    path_to_models_dir = f'{os.getcwd()}/models/{session_id}'
    is_exist = os.path.exists(path_to_models_dir)
    if not is_exist:
        os.makedirs(path_to_models_dir)
    return path_to_models_dir


@router.post("/{session_id:int}/upload_dataset", status_code=status.HTTP_200_OK)
async def upload_dataset(session_id: int, file: UploadFile):
    try:
        file_extension = pathlib.Path(file.filename).suffix.lower()
        if file_extension == '.rar' or file_extension == '.zip':
            path_to_dir = f'{os.getcwd()}/dataset/{session_id}'
            is_exist = os.path.exists(path_to_dir)
            if not is_exist:
                os.makedirs(path_to_dir)
            with open(f'{file.filename}', "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            if file_extension == ',rar':
                rf = rarfile.RarFile(file.file)
                rf.extractall(path_to_dir)
            else:
                file_name = file.filename
                # Write the contents of the UploadFile object to disk
                with open(f"{path_to_dir}/{file_name}", 'wb') as f:
                    while True:
                        chunk = await file.read(512 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                with zipfile.ZipFile(file_name, 'r') as zip_ref:
                    zip_ref.extractall(path_to_dir)
                os.remove(path_to_dir + "/" + file_name)
            os.remove(file.filename)
            model_path = make_model_folder(session_id)
            get_response = get_session(session_id)
            if get_response.status_code == status.HTTP_200_OK:
                body = json_to_schema(get_response.body, UserSession)
                update = UserSessionSummary(dataset_path=path_to_dir + "/",
                                            data_markup_path=body.data_markup_path,
                                            model_path=model_path + "/",
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
        logging.error(f"{traceback.format_exc()}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not upload dataset file")


@router.post("/{session_id:int}/upload_markup", status_code=status.HTTP_200_OK)
def upload_markup(session_id: int, file: UploadFile):
    try:
        if pathlib.Path(file.filename).suffix.lower() == '.pirogovjson':
            path_to_markup = f'{os.getcwd()}/markup/{session_id}_markup.json'
            with open(f'{file.filename}', "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            shutil.move(file.filename, path_to_markup)
            get_response = get_session(session_id)
            if get_response.status_code == status.HTTP_200_OK:
                body = json_to_schema(get_response.body, UserSession)
                update = UserSessionSummary(dataset_path=body.dataset_path,
                                            data_markup_path=path_to_markup,
                                            model_path=body.model_path,
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
