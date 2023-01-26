#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import status
from fastapi.responses import JSONResponse


class Connection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mariadb.connect(
                user="root",
                password="",
                host="mariadb-pirogov.net",
                port=3306,
                database="auto_model_learning")
            self.cursor = self.connection.cursor()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=self.connection)
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content=f"Error connecting to MariaDB Platform: {e}")
