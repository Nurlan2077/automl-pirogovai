#!/usr/bin/env python
# coding: utf-8

from fastapi import FastAPI, Request
from starlette.responses import Response

from routers import LossFunctionsRouter, OptimizersRouter, MetricsRouter, ModelsRouter, UserSessionsRouter, \
    FeaturesCnnRouter, ModelMetricsRouter, UsersRouter
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

app = FastAPI()

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Request-Method"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Request-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


app.include_router(MetricsRouter.router)
app.include_router(ModelsRouter.router)
app.include_router(LossFunctionsRouter.router)
app.include_router(FeaturesCnnRouter.router)
app.include_router(OptimizersRouter.router)
app.include_router(UsersRouter.router)
app.include_router(UserSessionsRouter.router)
app.include_router(ModelMetricsRouter.router)


@app.get("/")
async def root():
    logging.info("Root application started successfully")


@app.options("/{full_path:path}")
def options_handler(r: Request, full_path: str | None):
    headers = {"Access-Control-Allow-Origin": "*",
               "Access-Control-Allow-Methods": "*",
               "Access-Control-Allow-Headers": "Content-Type"}
    return Response(status_code=200, headers=headers)
