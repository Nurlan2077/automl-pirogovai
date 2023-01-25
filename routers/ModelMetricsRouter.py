#!/usr/bin/env python
# coding: utf-8

from Connection import Connection
from fastapi import APIRouter, status, Response
from models import ModelMetric
import mariadb


def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response


router = APIRouter(prefix="/model-metrics",
                   tags=["model-metrics"],
                   responses={404: {"description": "Model metrics router not found"}})


def compare_model_metrics(old_metric, new_metric):
    updates = []
    for old_pair, new_pair in zip(old_metric, new_metric):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates


def make_update_statement(metric_id, model_id, updates):
    statement = "update model_metric set "
    updates_row = []
    inserts = []
    for pair in updates:
        updates_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(model_id)
    inserts.append(metric_id)
    statement += ", ".join(updates_row) + " where model_id = ? and metric_id = ?"
    return statement, (*inserts,)


def init_router():
    response = connect()
    if response.status_code != 200:
        return response
    else:
        connection = response.body
        cursor = response.body.cursor()

        @router.post("/", status_code=status.HTTP_201_CREATED)
        def add_model_metric(model_metric_body: ModelMetric, response: Response):
            try:
                cursor.execute(
                    "insert into model_metric(model_id, metric_id, metric_value) values (?, ?, ?)",
                    (model_metric_body.model_id, model_metric_body.metric_id, model_metric_body.metric_value))
                connection.commit()
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not create model metric with body: {str(model_metric_body)}"

        @router.delete("/{metric_id}-{model_id}", status_code=status.HTTP_200_OK)
        def delete_model_metric(metric_id: int, model_id: int, response: Response):
            try:
                cursor.execute("delete from model_metric where metric_id = ? and model_id = ?", (metric_id, model_id))
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not delete model metric with metric id = {str(metric_id)} and model id = {str(model_id)}"

        @router.put("/{metric_id}-{model_id}", status_code=status.HTTP_200_OK)
        def update_model_metric(metric_id: int, model_id: int, model_metric_body: ModelMetric, response: Response):
            old_metric = get_model_metric(model_id, metric_id, response)
            if response.status_code == 200:
                metric = ModelMetric(metric_id=model_metric_body.metric_id, model_id=model_metric_body.model_id,
                                     metric_value=model_metric_body.metric_value)
                updates = compare_model_metrics(old_metric, metric)
                statement, inserts = make_update_statement(metric_id, updates)
                if len(inserts) > 1:
                    try:
                        cursor.execute(statement, inserts)
                        connection.commit()
                    except mariadb.Error as e:
                        response.status_code = status.HTTP_400_BAD_REQUEST
                        response.body = f"Could not update model metric with body: {str(model_metric_body)}"

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_model_metrics(response: Response):
            try:
                cursor.execute("select * from model_metric")
                metrics = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        metrics.append(ModelMetric(model_id=row[0], metric_id=row[1], metric_value=row[2]))
                return metrics
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = "Could not get model metrics, error = {e}"

        @router.get("/{metric_id}", status_code=status.HTTP_200_OK)
        def get_model_metric(model_id: int, metric_id: int, response: Response):
            try:
                cursor.execute("select * from model_metric where metric_id = ? and model_id = ?", (metric_id, model_id))
                metric_raw = cursor.fetchall()
                if len(metric_raw) == 0:
                    raise mariadb.Error(
                        f"Model metric with model id = {model_id} and metric id = {metric_id} not found")
            except mariadb.Error as e:
                response.status_code = status.HTTP_404_NOT_FOUND
                response.body = f"Model metric with model id = {model_id} and metric id = {metric_id} not found"
            model_metric = ModelMetric(id=metric_raw[0][0], metric_id=metric_raw[0][1],
                                       metric_value=metric_raw[0][2])
            return model_metric


init_router()
