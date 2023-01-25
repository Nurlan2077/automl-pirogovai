#!/usr/bin/env python
# coding: utf-8

from Connection import Connection
from fastapi import APIRouter, status, Response
from models import LossFunction, LossFunctionSummary
import mariadb


def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response


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


def init_router():
    response = connect()
    if response.status_code != 200:
        return response
    else:
        connection = response.body
        cursor = response.body.cursor()

        @router.post("/", status_code=status.HTTP_201_CREATED)
        def add_loss_function(loss_function_body: LossFunctionSummary, response: Response):
            try:
                cursor.execute("insert into loss_function(name) values (?)", (loss_function_body.name,))
                connection.commit()
            except Exception as e:
                response.body = f"Could not create loss function with body: {str(loss_function_body)}"
                response.status_code = status.HTTP_400_BAD_REQUEST

        @router.delete("/{loss_function_id}", status_code=status.HTTP_200_OK)
        def delete_loss_function(loss_function_id: int, response: Response):
            try:
                cursor.execute("delete from loss_function where id = ?", (loss_function_id,))
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not delete loss function with id = {str(loss_function_id)}"

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_loss_functions(response: Response):
            try:
                cursor.execute("select * from loss_function")
                loss_functions = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        loss_functions.append(LossFunction(id=row[0], name=row[1]))
                return loss_functions
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = "Could not get loss functions, error = {e}"

        @router.get("/{loss_function_id}", status_code=status.HTTP_200_OK)
        def get_loss_function(loss_function_id: int, response: Response):
            try:
                cursor.execute("select * from loss_function where id = ?", (loss_function_id,))
                function_raw = cursor.fetchall()
                if len(function_raw) == 0:
                    raise mariadb.Error(f"Loss function with id = {loss_function_id} not found")
            except mariadb.Error as e:
                response.status_code = status.HTTP_404_NOT_FOUND
                response.body = f"Loss function with id = {loss_function_id} not found"
            loss_function = LossFunction(id=function_raw[0][0], name=function_raw[0][1])
            return loss_function

        @router.put("/{loss_function_id}", status_code=status.HTTP_200_OK)
        def update_loss_function(loss_function_id: int, loss_function: LossFunctionSummary, response: Response):
            old_loss_function = get_loss_function(loss_function_id, response)
            loss_function = LossFunction(id=loss_function_id, name=loss_function.name)
            updates = compare_functions(old_loss_function, loss_function)
            statement, inserts = make_update_statement(loss_function_id, updates)
            if len(inserts) > 1:
                try:
                    cursor.execute(statement, inserts)
                    connection.commit()
                except mariadb.Error as e:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    response.body = f"Could not update loss function with body: {str(loss_function)}"


init_router()
