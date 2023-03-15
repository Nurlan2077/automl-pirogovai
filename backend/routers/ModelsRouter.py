#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import Model, ModelSummary
import logging

from .utils import get_created_id

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/models",
                   tags=["models"],
                   responses={404: {"description": "model router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_model(model_body: ModelSummary):
    try:
        cursor.execute(
            "insert into model(session_id, name, features_cnn_id, optimizer_id, loss_function_id, "
            "augmentation, learning_speed, epoch_count) values (?, ?, ?, ?, ?, ?, ?, ?)",
            (model_body.session_id, model_body.name, model_body.features_cnn_id,
             model_body.optimizer_id, model_body.loss_function_id, model_body.augmentation,
             model_body.learning_speed, model_body.epoch_count))
        connection.commit()
        entity_id = get_created_id(cursor, "model")[0][0]
        logging.info(f"Model with body = {str(model_body)} has been created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": entity_id})
    except mariadb.Error as e:
        logging.error(f"Could not create model with body: {str(model_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create model with body: {str(model_body)}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_models():
    try:
        cursor.execute("select * from model")
        models = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                models.append(Model(id=row[0], session_id=row[1], name=row[2],
                                    features_cnn_id=row[3], optimizer_id=row[4], loss_function_id=row[5],
                                    augmentation=row[6], learning_speed=row[7], epoch_count=row[8]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(models))
    except mariadb.Error as e:
        logging.error(f"Could not get models. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get models")


@router.delete("/{model_id}", status_code=status.HTTP_200_OK)
def delete_model(model_id: int):
    get_response = get_model(model_id)
    if get_response.status_code == status.HTTP_200_OK:
        try:
            cursor.execute("delete from model where id = ?", (model_id,))
            connection.commit()
            logging.info(f"Model with id = {str(model_id)} has been deleted successfully")
        except mariadb.Error as e:
            logging.error(f"Could not delete model with id = {str(model_id)}. Error: {e}")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Could not delete model with id = {str(model_id)}")
    else:
        logging.error(f"Could not delete model with id = {str(model_id)}. Error: entity does not exist.")
        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                     content=f"Could not delete model with id = {str(model_id)} because entity does not exist.")


@router.get("/{model_id}", status_code=status.HTTP_200_OK)
def get_model(model_id: int):
    try:
        cursor.execute("select * from model where id = ?", (model_id,))
        row = cursor.fetchall()
        if len(row) == 0:
            logging.warning(f"Model with id = {model_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Model with id = {model_id} not found")
        model = Model(id=row[0][0], session_id=row[0][1], name=row[0][2],
                      features_cnn_id=row[0][3], optimizer_id=row[0][4], loss_function_id=row[0][5],
                      augmentation=row[0][6], learning_speed=row[0][7], epoch_count=row[0][8])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(model))
    except mariadb.Error as e:
        logging.error(f"Could not get model with id = {model_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get model with id = {model_id}")
