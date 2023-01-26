#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import Optimizer, OptimizerSummary, json_to_schema
from .utils import compare_items, make_update_statement
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/optimizers",
                   tags=["optimizers"],
                   responses={404: {"description": "Optimizer router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_optimizer(optimizer_body: OptimizerSummary):
    try:
        cursor.execute("insert into optimizer(name) values (?)", (optimizer_body.name,))
        connection.commit()
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create optimizer with body: {str(optimizer_body)}")


@router.delete("/{optimizer_id}", status_code=status.HTTP_200_OK)
def delete_optimizer(optimizer_id: int):
    try:
        cursor.execute("delete from optimizer where id = ?", (optimizer_id,))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete optimizer with id = {str(optimizer_id)}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_optimizers():
    try:
        cursor.execute("select * from optimizer")
        optimizers = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                optimizers.append(Optimizer(id=row[0], name=row[1]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(optimizers))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get optimizers")


@router.get("/{optimizer_id}", status_code=status.HTTP_200_OK)
def get_optimizer(optimizer_id: int):
    try:
        cursor.execute("select * from optimizer where id = ?", (optimizer_id,))
        feature_raw = cursor.fetchall()
        if len(feature_raw) == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Optimizer with id = {optimizer_id} not found")
        optimizer = Optimizer(id=feature_raw[0][0], name=feature_raw[0][1])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(optimizer))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get optimizer with id = {optimizer_id}")


@router.put("/{optimizer_id}", status_code=status.HTTP_200_OK)
def update_optimizer(optimizer_id: int, optimizer: OptimizerSummary):
    get_response = get_optimizer(optimizer_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_optimizer = json_to_schema(get_response.body, Optimizer)
        optimizer = Optimizer(id=optimizer_id, name=optimizer.name)
        updates = compare_items(old_optimizer, optimizer)
        statement, inserts = make_update_statement([optimizer_id], "optimizer", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update optimizer with body: {str(optimizer)}")
    else:
        return get_response
