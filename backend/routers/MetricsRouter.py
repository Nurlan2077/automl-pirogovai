#!/usr/bin/env python
# coding: utf-8
import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import Metric, MetricSummary, json_to_schema
from .utils import compare_items, make_update_statement
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
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create metric with body: {str(metric_body)}")


@router.delete("/{metric_id}", status_code=status.HTTP_200_OK)
def delete_metric(metric_id: int):
    try:
        cursor.execute("delete from metric where id = ?", (metric_id,))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete metric with id = {str(metric_id)}")


@router.put("/{metric_id}", status_code=status.HTTP_200_OK)
def update_metric(metric_id: int, metric_body: MetricSummary):
    get_response = get_metric(metric_id)
    if get_response.status_code == 200:
        old_metric = json_to_schema(get_response.body, Metric)
        metric = Metric(id=metric_id, name=metric_body.name)
        updates = compare_items(old_metric, metric)
        statement, inserts = make_update_statement([metric_id], "metric", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
            except mariadb.Error:
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
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get metrics")


@router.get("/{metric_id}", status_code=status.HTTP_200_OK)
def get_metric(metric_id: int):
    try:
        cursor.execute("select * from metric where id = ?", (metric_id,))
        metric_raw = cursor.fetchall()
        if len(metric_raw) == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Metric with id = {metric_id} not found")
        metric = Metric(id=metric_raw[0][0], name=metric_raw[0][1])
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(metric))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get metric with id = {metric_id}")
