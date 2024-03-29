#!/usr/bin/env python
# coding: utf-8
import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import Metric, MetricSummary, json_to_schema
from .utils import compare_items, make_update_statement, get_created_id
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/metrics",
                   tags=["metrics"],
                   responses={404: {"description": "Metrics router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_metric(metric_body: MetricSummary):
    try:
        cursor.execute(
            "insert into metric(name) values (?)",
            (metric_body.name,))
        connection.commit()
        entity_id = get_created_id(cursor, "metric")[0][0]
        logging.info(f"Metric with body = {str(metric_body)} has been created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": entity_id})
    except mariadb.Error as e:
        logging.error(f"Could not create metric with body: {str(metric_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create metric with body: {str(metric_body)}")


@router.delete("/{metric_id}", status_code=status.HTTP_200_OK)
def delete_metric(metric_id: int):
    get_response = get_metric(metric_id)
    if get_response.status_code == status.HTTP_200_OK:
        try:
            cursor.execute("delete from metric where id = ?", (metric_id,))
            connection.commit()
            logging.info(f"Metric with id = {str(metric_id)} has been deleted successfully")
        except mariadb.Error as e:
            logging.error(f"Could not delete metric with id = {str(metric_id)}. Error: {e}")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Could not delete metric with id = {str(metric_id)}")
    else:
        logging.error(f"Could not delete metric with id = {str(metric_id)}. Error: entity does not exist.")
        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                     content=f"Could not delete metric with id = {str(metric_id)} because entity does not "
                             f"exist.")


@router.put("/{metric_id}", status_code=status.HTTP_200_OK)
def update_metric(metric_id: int, metric_body: MetricSummary):
    get_response = get_metric(metric_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_metric = json_to_schema(get_response.body, Metric)
        metric = Metric(id=metric_id, name=metric_body.name)
        updates = compare_items(old_metric, metric)
        statement, inserts = make_update_statement([metric_id], "metric", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
                logging.info(f"Metric with id = {metric_id} has been updated successfully")
            except mariadb.Error as e:
                logging.error(f"Could not update metric with body: {str(metric_body)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update metric with body: {str(metric_body)}")
    else:
        return get_response


@router.get("/", status_code=status.HTTP_200_OK)
def get_metrics():
    try:
        cursor.execute("select * from metric")
        metrics = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                metrics.append(Metric(id=row[0], name=row[1]))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(metrics))
    except mariadb.Error as e:
        logging.error(f"Could not get metrics. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get metrics")


@router.get("/by-name/{metric_name}", status_code=status.HTTP_200_OK)
def get_metric_by_name(metric_name: str):
    try:
        cursor.execute("select * from metric where name = ?", (metric_name,))
        metric_raw = cursor.fetchall()
        if len(metric_raw) == 0:
            logging.warning(f"Metric with name = {metric_name} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Metric with name = {metric_name} not found")
        metric = Metric(id=metric_raw[0][0], name=metric_raw[0][1])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(metric))
    except mariadb.Error as e:
        logging.error(f"Could not get metric with name = {metric_name}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get metric with name = {metric_name}")


@router.get("/{metric_id}", status_code=status.HTTP_200_OK)
def get_metric(metric_id: int):
    try:
        cursor.execute("select * from metric where id = ?", (metric_id,))
        metric_raw = cursor.fetchall()
        if len(metric_raw) == 0:
            logging.warning(f"Metric with id = {metric_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Metric with id = {metric_id} not found")
        metric = Metric(id=metric_raw[0][0], name=metric_raw[0][1])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(metric))
    except mariadb.Error as e:
        logging.error(f"Could not get metric with id = {metric_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get metric with id = {metric_id}")
