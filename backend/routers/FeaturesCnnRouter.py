#!/usr/bin/env python
# coding: utf-8
import mariadb
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .connection import Connection
from .models import FeatureCnn, FeatureCnnSummary, json_to_schema
from .utils import compare_items, make_update_statement, get_created_id
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:%(asctime)s%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

connection, cursor = Connection().try_to_connect()

router = APIRouter(prefix="/features-cnn",
                   tags=["features-cnns"],
                   responses={404: {"description": "Features cnn router not found"}})


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_feature_cnn(feature_cnn_body: FeatureCnnSummary):
    try:
        cursor.execute("insert into features_cnn(name) values (?)", (feature_cnn_body.name,))
        connection.commit()
        entity_id = get_created_id(cursor, "features_cnn")[0][0]
        logging.info(f"Feature cnn with body = {str(feature_cnn_body)} has been created successfully")
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": entity_id})
    except mariadb.Error as e:
        logging.error(f"Could not create feature cnn with body: {str(feature_cnn_body)}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not create feature cnn with body: {str(feature_cnn_body)}")


@router.delete("/{feature_cnn_id}", status_code=status.HTTP_200_OK)
def delete_feature_cnn(feature_cnn_id: int):
    get_response = get_feature_cnn(feature_cnn_id)
    if get_response.status_code == status.HTTP_200_OK:
        try:
            cursor.execute("delete from features_cnn where id = ?", (feature_cnn_id,))
            connection.commit()
            logging.info(f"feature cnn with id = {feature_cnn_id} has been deleted successfully")
        except mariadb.Error as e:
            logging.error(f"Could not delete feature cnn with id = {str(feature_cnn_id)}. Error: {e}")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=f"Could not delete feature cnn with id = {str(feature_cnn_id)}")
    else:
        logging.error(f"Could not delete feature cnn with id = {str(feature_cnn_id)}. Error: entity does not exist.")
        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                     content=f"Could not delete feature cnn with id = {str(feature_cnn_id)} because entity does not "
                             f"exist.")


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
    except mariadb.Error as e:
        logging.error(f"Could not get feature cnns. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="Could not get feature cnns")


@router.get("/{feature_cnn_id}", status_code=status.HTTP_200_OK)
def get_feature_cnn(feature_cnn_id: int):
    try:
        cursor.execute("select * from features_cnn where id = ?", (feature_cnn_id,))
        feature_raw = cursor.fetchall()
        if len(feature_raw) == 0:
            logging.warning(f"Feature cnn with id = {feature_cnn_id} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Feature cnn with id = {feature_cnn_id} not found")
        feature_cnn = FeatureCnn(id=feature_raw[0][0], name=feature_raw[0][1])
        return JSONResponse(content=jsonable_encoder(feature_cnn))
    except mariadb.Error as e:
        logging.error(f"Could not get feature cnn with id = {feature_cnn_id}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get feature cnn with id = {feature_cnn_id}")


@router.get("/by-name/{feature_cnn_name}", status_code=status.HTTP_200_OK)
def get_feature_cnn_by_name(feature_cnn_name: str):
    try:
        cursor.execute("select * from features_cnn where name = ?", (feature_cnn_name,))
        feature_raw = cursor.fetchall()
        if len(feature_raw) == 0:
            logging.warning(f"Feature cnn with name = {feature_cnn_name} not found")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Feature cnn with name = {feature_cnn_name} not found")
        feature_cnn = FeatureCnn(id=feature_raw[0][0], name=feature_raw[0][1])
        return JSONResponse(content=jsonable_encoder(feature_cnn))
    except mariadb.Error as e:
        logging.error(f"Could not get feature cnn with bane = {feature_cnn_name}. Error: {e}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Could not get feature cnn with name = {feature_cnn_name}")


@router.put("/{feature_cnn_id}", status_code=status.HTTP_200_OK)
def update_feature_cnn(feature_cnn_id: int, feature_cnn: FeatureCnnSummary):
    get_response = get_feature_cnn(feature_cnn_id)
    if get_response.status_code == status.HTTP_200_OK:
        old_feature_cnn = json_to_schema(get_response.body, FeatureCnn)
        feature_cnn = FeatureCnn(id=feature_cnn_id, name=feature_cnn.name)
        updates = compare_items(old_feature_cnn, feature_cnn)
        statement, inserts = make_update_statement([feature_cnn_id], "features_cnn", ["id"], updates)
        if len(inserts) > 1:
            try:
                cursor.execute(statement, inserts)
                connection.commit()
                logging.info(f"Feature cnn with id = {feature_cnn_id} has been updated successfully")
            except mariadb.Error as e:
                logging.error(f"Could not update feature cnn with body: {str(feature_cnn)}. Error: {e}")
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content=f"Could not update feature cnn with body: {str(feature_cnn)}")
    else:
        return get_response
