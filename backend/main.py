#!/usr/bin/env python
# coding: utf-8

from fastapi import FastAPI
from routers import LossFunctionsRouter, OptimizersRouter, MetricsRouter, ModelsRouter, UserSessionsRouter, \
    FeaturesCnnRouter, ModelMetricsRouter, UsersRouter

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


