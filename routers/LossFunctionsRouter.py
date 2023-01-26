#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from Connection import Connection
from .models import LossFunction, LossFunctionSummary, json_to_schema

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/loss-functions",
                   tags=["loss-functions"],
                   responses={404: {"description": "Loss functions router not found"}})


def compare_functions(old_function, new_function):
    updates = []
    for old_pair, new_pair in zip(old_function, new_function):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates


def make_update_statement(loss_function_id, updates):
    statement = "update loss_function set "
    updates_row = []
    inserts = []
    for pair in updates:
        updates_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(loss_function_id)
    statement += ", ".join(updates_row) + " where id = ?"
    return statement, (*inserts,)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_loss_function(loss_function_body: LossFunctionSummary):
    try:
        cursor.execute("insert into loss_function(name) values (?)", (loss_function_body.name,))
        connection.commit()
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create loss function with body: {str(loss_function_body)}")


@router.delete("/{loss_function_id}", status_code=status.HTTP_200_OK)
def delete_loss_function(loss_function_id: int):
    try:
        cursor.execute("delete from loss_function where id = ?", (loss_function_id,))
    except mariadb.Error:
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
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get loss functions")


@router.get("/{loss_function_id}", status_code=status.HTTP_200_OK)
def get_loss_function(loss_function_id: int):
    try:
        cursor.execute("select * from loss_function where id = ?", (loss_function_id,))
        function_raw = cursor.fetchall()
        if len(function_raw) == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Loss function with id = {loss_function_id} not found")
        loss_function = LossFunction(id=function_raw[0][0], name=function_raw[0][1])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(loss_function))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get loss function with id = {loss_function_id}")


@router.put("/{loss_function_id}", status_code=status.HTTP_200_OK)
def update_loss_function(loss_function_id: int, loss_function: LossFunctionSummary):
    get_response = get_loss_function(loss_function_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_loss_function = json_to_schema(get_response.body, LossFunction)
        loss_function = LossFunction(id=loss_function_id, name=loss_function.name)
        updates = compare_functions(old_loss_function, loss_function)
        statement, inserts = make_update_statement(loss_function_id, updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update loss function with body: {str(loss_function)}")
    else:
        return get_response
