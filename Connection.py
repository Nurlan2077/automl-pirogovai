#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import Response, status

class Connection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self, response):
        try:
            self.connection = mariadb.connect(
                                user="root",
                                password="",
                                host="127.0.0.1",
                                port=3306,
                                database="auto_model_learning")
            self.cursor = self.connection.cursor()
            response.status_code = status.HTTP_200_OK
            response.body = self.connection
        except mariadb.Error as e:
            response.status_code = status.HTTP_500_Internal_Server_Error
            response.body = f"Error connecting to MariaDB Platform: {e}"

