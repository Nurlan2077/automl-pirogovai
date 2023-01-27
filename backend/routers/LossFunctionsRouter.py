#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import LossFunction, LossFunctionSummary, json_to_schema
from .utils import compare_items, make_update_statement
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/loss-functions",
                   tags=["loss-functions"],
                   responses={404: {"description": "Loss functions router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_loss_function(loss_function_body: LossFunctionSummary):
    try:
        cursor.execute("insert into loss_function(name) values (?)", (loss_function_body.name,))
        connection.commit()
        logging.info(f"Loss function with body = {str(loss_function_body)} has been created successfully")
    except mariadb.Error as e:
        logging.error(f"Could not create loss function with body: {str(loss_function_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create loss function with body: {str(loss_function_body)}")


@router.delete("/{loss_function_id}", status_code=status.HTTP_200_OK)
def delete_loss_function(loss_function_id: int):
    try:
        cursor.execute("delete from loss_function where id = ?", (loss_function_id,))
        logging.info(f"Loss function with id = {str(loss_function_id)} has been deleted successfully")
    except mariadb.Error as e:
        logging.error(f"Could not delete loss function with id = {str(loss_function_id)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete loss function with id = {str(loss_function_id)}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_loss_functions():
    try:
        cursor.execute("select * from loss_function")
        loss_functions = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                loss_functions.append(LossFunction(id=row[0], name=row[1]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(loss_functions))
    except mariadb.Error as e:
        logging.error(f"Could not get loss functions. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get loss functions")


@router.get("/{loss_function_id}", status_code=status.HTTP_200_OK)
def get_loss_function(loss_function_id: int):
    try:
        cursor.execute("select * from loss_function where id = ?", (loss_function_id,))
        function_raw = cursor.fetchall()
        if len(function_raw) == 0:
            logging.warning(f"Loss function with id = {loss_function_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Loss function with id = {loss_function_id} not found")
        loss_function = LossFunction(id=function_raw[0][0], name=function_raw[0][1])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(loss_function))
    except mariadb.Error as e:
        logging.error(f"Could not get loss function with id = {loss_function_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get loss function with id = {loss_function_id}")


@router.put("/{loss_function_id}", status_code=status.HTTP_200_OK)
def update_loss_function(loss_function_id: int, loss_function: LossFunctionSummary):
    get_response = get_loss_function(loss_function_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_loss_function = json_to_schema(get_response.body, LossFunction)
        loss_function = LossFunction(id=loss_function_id, name=loss_function.name)
        updates = compare_items(old_loss_function, loss_function)
        statement, inserts = make_update_statement([loss_function_id], "loss_function", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
            except mariadb.Error as e:
                logging.error(f"Could not update loss function with body: {str(loss_function)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update loss function with body: {str(loss_function)}")
    else:
        return get_response
