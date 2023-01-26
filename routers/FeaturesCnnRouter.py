#!/usr/bin/env python
# coding: utf-8
import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from Connection import Connection
from .models import FeatureCnn, FeatureCnnSummary, json_to_schema

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/features-cnn",
                   tags=["features-cnns"],
                   responses={404: {"description": "Features cnn router not found"}})


def compare_features(old_feature, new_feature):
    updates = []
    for old_pair, new_pair in zip(old_feature, new_feature):
        if old_pair[1] != new_pair[1]:
            updates.append((new_pair[0], new_pair[1]))
    return updates


def make_update_statement(feature_cnn_id, updates):
    statement = "update features_cnn set "
    updates_row = []
    inserts = []
    for pair in updates:
        updates_row.append(f"{pair[0]} = ?")
        inserts.append(pair[1])
    inserts.append(feature_cnn_id)
    statement += ", ".join(updates_row) + " where id = ?"
    return statement, (*inserts,)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_feature_cnn(feature_cnn_body: FeatureCnnSummary):
    try:
        cursor.execute("insert into features_cnn(name) values (?)", (feature_cnn_body.name,))
        connection.commit()
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create feature cnn with body: {str(feature_cnn_body)}")


@router.delete("/{feature_cnn_id}", status_code=status.HTTP_200_OK)
def delete_feature_cnn(feature_cnn_id: int):
    try:
        cursor.execute("delete from features_cnn where id = ?", (feature_cnn_id,))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not delete feature cnn with id = {str(feature_cnn_id)}")


@router.get("/", status_code=status.HTTP_200_OK)
def get_feature_cnns():
    try:
        cursor.execute("select * from features_cnn")
        feature_cnns = []
        result = cursor.fetchall()
        if len(result) > 0:
            for row in result:
                feature_cnns.append(FeatureCnn(id=row[0], name=row[1]))
        return jsonable_encoder(feature_cnns)
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get feature cnns")


@router.get("/{feature_cnn_id}", status_code=status.HTTP_200_OK)
def get_feature_cnn(feature_cnn_id: int):
    try:
        cursor.execute("select * from features_cnn where id = ?", (feature_cnn_id,))
        feature_raw = cursor.fetchall()
        if len(feature_raw) == 0:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Feature cnn with id = {feature_cnn_id} not found")
        feature_cnn = FeatureCnn(id=feature_raw[0][0], name=feature_raw[0][1])
        return JSONResponse(content=jsonable_encoder(feature_cnn))
    except mariadb.Error:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get feature cnn with id = {feature_cnn_id}")


@router.put("/{feature_cnn_id}", status_code=status.HTTP_200_OK)
def update_feature_cnn(feature_cnn_id: int, feature_cnn: FeatureCnnSummary):
    get_response = get_feature_cnn(feature_cnn_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_feature_cnn = json_to_schema(get_response.body, FeatureCnn)
        feature_cnn = FeatureCnn(id=feature_cnn_id, name=feature_cnn.name)
        updates = compare_features(old_feature_cnn, feature_cnn)
        statement, inserts = make_update_statement(feature_cnn_id, updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
            except mariadb.Error:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update feature cnn with body: {str(feature_cnn)}")
    else:
        return get_response
