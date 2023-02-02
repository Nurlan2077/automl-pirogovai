#!/usr/bin/env python
# coding: utf-8

import mariadb
from fastapi import status
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


class Connection:
    def __init__(self):
        self.status_code = status.HTTP_201_CREATED
        self.body = None

    def set(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def connect(self):
        try:
            connection = mariadb.connect(
                user="root",
                password="",
                host="mariadb-pirogov.net",
                port=3306,
                database="auto_model_learning")
            self.set(status.HTTP_200_OK, connection)
        except Exception as e:
            self.set(status.HTTP_200_OK, "Error connecting to MariaDB Platform:")
            logging.error(f"Error connecting to MariaDB Platform: {e}")

    def try_to_connect(self, times=3):
        connection = None
        cursor = None
        for i in range(times):
            self.connect()
            if self.status_code == status.HTTP_200_OK:
                break
        if self.status_code == status.HTTP_200_OK:
            connection = self.body
            cursor = connection.cursor()
        return connection, cursor
