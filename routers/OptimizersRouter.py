#!/usr/bin/env python
# coding: utf-8

from Connection import Connection
from fastapi import APIRouter, status, Response
from models import Optimizer, OptimizerSummary
import mariadb


def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response


router = APIRouter(prefix="/optimizers",
                   tags=["optimizers"],
                   responses={404: {"description": "Optimizer router not found"}})


def compare_optimizers(old_optimizer, new_optimizer):
    updates = []
    for old_pair, new_pair in zip(old_optimizer, new_optimizer):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates


def make_update_statement(optimizer_id, updates):
    statement = "update optimizer set "
    updates_row = []
    inserts = []
    for pair in updates:
        updates_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(optimizer_id)
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
        def add_optimizer(optimizer_body: OptimizerSummary, response: Response):
            try:
                cursor.execute("insert into optimizer(name) values (?)", (optimizer_body.name,))
                connection.commit()
            except Exception as e:
                response.body = f"Could not create optimizer with body: {str(optimizer_body)}"
                response.status_code = status.HTTP_400_BAD_REQUEST

        @router.delete("/{optimizer_id}", status_code=status.HTTP_200_OK)
        def delete_optimizer(optimizer_id: int, response: Response):
            try:
                cursor.execute("delete from optimizer where id = ?", (optimizer_id,))
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not delete optimizer with id = {str(optimizer_id)}"

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_optimizers(response: Response):
            try:
                cursor.execute("select * from optimizer")
                optimizers = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        optimizers.append(Optimizer(id=row[0], name=row[1]))
                return optimizers
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = "Could not get optimizers, error = {e}"

        @router.get("/{optimizer_id}", status_code=status.HTTP_200_OK)
        def get_optimizer(optimizer_id: int, response: Response):
            try:
                cursor.execute("select * from optimizer where id = ?", (optimizer_id,))
                feature_raw = cursor.fetchall()
                if len(feature_raw) == 0:
                    raise mariadb.Error(f"Optimizer with id = {optimizer_id} not found")
            except mariadb.Error as e:
                response.status_code = status.HTTP_404_NOT_FOUND
                response.body = f"Optimizer with id = {optimizer_id} not found"
            optimizer = Optimizer(id=feature_raw[0][0], name=feature_raw[0][1])
            return optimizer

        @router.put("/{optimizer_id}", status_code=status.HTTP_200_OK)
        def update_optimizer(optimizer_id: int, optimizer: OptimizerSummary, response: Response):
            old_optimizer = get_optimizer(optimizer_id, response)
            optimizer = Optimizer(id=optimizer_id, name=optimizer.name)
            updates = compare_optimizers(old_optimizer, optimizer)
            statement, inserts = make_update_statement(optimizer_id, updates)
            if len(inserts) > 1:
                try:
                    cursor.execute(statement, inserts)
                    connection.commit()
                except mariadb.Error as e:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    response.body = f"Could not update optimizer with body: {str(optimizer)}"


init_router()
