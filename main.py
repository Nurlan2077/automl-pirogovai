#!/usr/bin/env python
# coding: utf-8
import uvicorn

from Connection import Connection
from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sys

if sys.path[0] + "/routers" not in sys.path:
    sys.path.append(sys.path[0] + "/routers")

import MetricsRouter
import ModelsRouter
import LossFunctionsRouter
import FeaturesCnnRouter
import OptimizersRouter
import UsersRouter
import UserSessionsRouter
import ModelMetricsRouter

app = FastAPI()
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
    return {"message": "Hello World"}


uvicorn.run(app, host="0.0.0.0", port=8000)
