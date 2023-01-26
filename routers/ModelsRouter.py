#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from Connection import Connection
from models import Model, ModelSummary


def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response


router = APIRouter(prefix="/models",
                   tags=["models"],
                   responses={404: {"description": "model router not found"}})


def init_router():
    response = connect()
    if response.status_code != 200:
        return response
    else:
        connection = response.body
        cursor = response.body.cursor()

        @router.post("/", status_code=status.HTTP_201_CREATED)
        def add_model(_model_body: ModelSummary):
            try:
                cursor.execute(
                    "insert into model(session_id, name, features_cnn_id, optimizer_id, loss_function_id, "
                    "augmentation, learning_speed, epoch_count) values (?, ?, ?, ?, ?, ?, ?, ?)",
                    (_model_body.session_id, _model_body.name, _model_body.features_cnn_id,
                     _model_body.optimizer_id, _model_body.loss_function_id, _model_body.augmentation,
                     _model_body.learning_speed, _model_body.epoch_count))
                connection.commit()
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not create model with body: {str(_model_body)}")

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_models():
            try:
                cursor.execute("select * from model")
                models = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        models.append(Model(id=row[0], session_id=row[1], name=row[2],
                                            features_cnn_id=row[3], optimizer_id=row[4], loss_functuion_id=row[5],
                                            augmetation=row[6], learning_speed=row[7], epoch_count=row[8]))
                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content=jsonable_encoder(models))
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content="Could not get models")

        @router.get("/{model_id}", status_code=status.HTTP_200_OK)
        def get_model(model_id: int):
            try:
                cursor.execute("select * from model where id = ?", (model_id,))
                row = cursor.fetchall()
                if len(row) == 0:
                    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                        content=f"Model with id = {model_id} not found")
                model = Model(id=row[0][0], session_id=row[0][1], name=row[0][2],
                              features_cnn_id=row[0][3], optimizer_id=row[0][4], loss_functuion_id=row[0][5],
                              augmetation=row[0][6], learning_speed=row[0][7], epoch_count=row[0][8])
                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content=jsonable_encoder(model))
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not get model with id = {model_id}")


init_router()
