#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import ModelMetric, json_to_schema, ModelMetricNamed
from .utils import compare_items, make_update_statement
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/model-metrics",
                   tags=["model-metrics"],
                   responses={404: {"description": "Model metrics router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_model_metric(model_metric_body: ModelMetric):
    try:
        cursor.execute(
            "insert into model_metric(model_id, metric_id, metric_value) values (?, ?, ?)",
            (model_metric_body.model_id, model_metric_body.metric_id, model_metric_body.metric_value))
        connection.commit()
        logging.info(f"Model metric with body = {str(model_metric_body)} has been created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"model_id": model_metric_body.model_id, "metric_id": model_metric_body.metric_id})

    except mariadb.Error as e:
        logging.error(f"Could not create model metric with body: {str(model_metric_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create model metric with body: {str(model_metric_body)}")


@router.delete("/{metric_id}-{model_id}", status_code=status.HTTP_200_OK)
def delete_model_metric(metric_id: int, model_id: int):
    try:
        cursor.execute("delete from model_metric where metric_id = ? and model_id = ?", (metric_id, model_id))
        logging.info(f"Model metric with id = {str(metric_id)} has been deleted successfully")
    except mariadb.Error as e:
        logging.error(f"Could not delete model metric with metric id = {str(metric_id)} and model id = {str(model_id)}."
                      f" Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete model metric with metric id = {str(metric_id)} and "
                                    f"model id = {str(model_id)}")


@router.put("/{metric_id}-{model_id}", status_code=status.HTTP_200_OK)
def update_model_metric(metric_id: int, model_id: int, model_metric_body: ModelMetric):
    get_response = get_model_metric(model_id, metric_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_model_metric = json_to_schema(get_response.body, ModelMetric)
        model_metric = ModelMetric(metric_id=model_metric_body.metric_id, model_id=model_metric_body.model_id,
                                   metric_value=model_metric_body.metric_value)
        updates = compare_items(old_model_metric, model_metric)
        statement, inserts = make_update_statement([metric_id, model_id], "model_metric", ["metric_id", "model_id"],
                                                   updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
                logging.info(f"Model metric with model_id = {model_id} and metric_id = {metric_id} has been updated "
                             f"successfully")
            except mariadb.Error as e:
                logging.error(f"Could not update model metric with body: {str(model_metric_body)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update model metric with body: {str(model_metric_body)}")
    else:
        return get_response


@router.get("/", status_code=status.HTTP_200_OK)
def get_models_metrics():
    try:
        cursor.execute("select * from model_metric")
        metrics = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                metrics.append(ModelMetric(model_id=row[0], metric_id=row[1], metric_value=row[2]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(metrics))
    except mariadb.Error as e:
        logging.error(f"Could not get model metrics. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get model metrics")


@router.get("/with-names/{model_id}", status_code=status.HTTP_200_OK)
def get_model_metrics_with_names(model_id: int):
    try:
        cursor.execute("select metric.name as metric_name, model.name as model_name, model_metric.metric_value "
                       "from model_metric "
                       "join metric on metric.id = model_metric.metric_id "
                       "join model on model_metric.model_id = model.id where model_id = ?", (model_id,))
        metrics = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                metrics.append(ModelMetricNamed(metric_name=row[0], model_name=row[1], metric_value=row[2]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(metrics))
    except mariadb.Error as e:
        logging.error(f"Could not get model metrics. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get model metrics")


@router.get("/{model_id}", status_code=status.HTTP_200_OK)
def get_model_metrics(model_id: int):
    try:
        cursor.execute("select * from model_metric where model_id = ?", (model_id,))
        metric_raw = cursor.fetchall()
        if len(metric_raw) == 0:
            logging.warning(f"Model metric with model id = {model_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Model metric with model id = {model_id} not found")
        model_metric = ModelMetric(id=metric_raw[0][0], metric_id=metric_raw[0][1],
                                   metric_value=metric_raw[0][2])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(model_metric))
    except mariadb.Error as e:
        logging.error(f"Could not get model metric with model id = {model_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get model metric with model id = {model_id}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_model_metric(model_id: int, metric_id: int):
    try:
        cursor.execute("select * from model_metric where metric_id = ? and model_id = ?", (metric_id, model_id))
        metric_raw = cursor.fetchall()
        if len(metric_raw) == 0:
            logging.warning(f"Model metric with model id = {model_id} and metric id = {metric_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Model metric with model id = {model_id} and metric id = {metric_id} "
                                        f"not found")
        model_metric = ModelMetric(id=metric_raw[0][0], metric_id=metric_raw[0][1],
                                   metric_value=metric_raw[0][2])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(model_metric))
    except mariadb.Error as e:
        logging.error(f"Could not get model metric with model id = {model_id} and metric id = {metric_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get model metric with model id = {model_id} "
                                    f"and metric id = {metric_id}")
