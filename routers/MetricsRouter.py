#!/usr/bin/env python
# coding: utf-8

from Connection import Connection
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import mariadb

class MetricSummary(BaseModel):
    name: str
    metric_value: float

class Metric(BaseModel):
    id: int
    name: str
    metric_value: float

def connect():
    response = Response()
    for i in range(3):
        response = Response()
        Connection().connect(response)
        if response.status_code == 200:
            break
    return response

router = APIRouter(prefix="/metrics",
                            tags=["metrics"],
                            responses={404: {"description": "Metrics router not found"}})

def compare_metrics(old_metric, new_metric):
    updates = []
    for old_pair, new_pair in zip(old_metric, new_metric):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates

def make_update_statement(metric_id, updates):
    statement = "update metric set "
    updates_row = []
    inserts = []
    for pair in updates:
        updates_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(metric_id)
    statement += ", ".join(updates_row) + " where id = ?"
    return statement, (*inserts, )

def init_router():
    response = connect()
    if response.status_code != 200:
        return response
    else:
        connection = response.body
        cursor = response.body.cursor()
        @router.post("/", status_code=status.HTTP_201_CREATED)
        def add_metric(metric_body: MetricSummary, response: Response):
            try:
                cursor.execute(
                "insert into metric(name, metric_value) values (?, ?)", 
                (metric_body.name, metric_body.metric_value))
                connection.commit()
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not create metric with body: {str(metric_body)}"
                
        @router.delete("/{metric_id}", status_code=status.HTTP_200_OK)
        def delete_metric(metric_id: int, response: Response):
            try:
                cursor.execute("delete from metric where id = ?", (metric_id,))
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = f"Could not delete metric with id = {str(metric_id)}"
                
        @router.put("/{metric_id}", status_code=status.HTTP_200_OK)        
        def update_metric(metric_id: int, metric_body: MetricSummary, response: Response):
            old_metric = get_metric(metric_id, response)
            if response.status_code == 200:
                metric = Metric(id=metric_id, name=metric_body.name, metric_value=metric_body.metric_value)
                updates = compare_metrics(old_metric, metric)
                statement, inserts = make_update_statement(metric_id, updates)
                if len(inserts) > 1:
                    try:
                        cursor.execute(statement, inserts)
                        connection.commit()
                    except mariadb.Error as e:
                        response.status_code = status.HTTP_400_BAD_REQUEST
                        response.body = f"Could not update metric with body: {str(metric_body)}"

        @router.get("/", status_code=status.HTTP_200_OK)
        def get_metrics(response: Response):
            try:
                cursor.execute("select * from metric")
                metrics = []
                result = cursor.fetchall()
                if len(result) > 0:
                    for row in result:
                        metrics.append(Metric(id=row[0], name=row[1], metric_value=row[2]))
                return metrics
            except mariadb.Error as e:
                response.status_code = status.HTTP_400_BAD_REQUEST
                response.body = "Could not get metrics, error = {e}"
    
        @router.get("/{metric_id}", status_code=status.HTTP_200_OK)
        def get_metric(metric_id: int, response: Response):
            try:
                cursor.execute("select * from metric where id = ?", (metric_id, ))
                metric_raw = cursor.fetchall()
                if len(metric_raw) == 0:
                    raise mariadb.Error(f"Metric with id = {metric_id} not found") 
            except mariadb.Error as e:
                response.status_code = status.HTTP_404_NOT_FOUND
                response.body = f"Metric with id = {metric_id} not found"
            metric = Metric(id=metric_raw[0][0], name=metric_raw[0][1], 
                        metric_value=metric_raw[0][2])
            return metric
            
init_router()
