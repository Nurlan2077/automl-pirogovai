import json
from typing import List

from pydantic import BaseModel, parse_obj_as


class FeatureCnnSummary(BaseModel):
    name: str


class FeatureCnn(BaseModel):
    id: int
    name: str


class LossFunctionSummary(BaseModel):
    name: str


class LossFunction(BaseModel):
    id: int
    name: str


class MetricSummary(BaseModel):
    name: str


class Metric(BaseModel):
    id: int
    name: str


class ModelMetric(BaseModel):
    model_id: int
    metric_id: int
    metric_value: float


class ModelMetricNamed(BaseModel):
    metric_name: str
    model_name: str
    metric_value: float


class HyperParam(BaseModel):
    name: str
    value: str


class HyperParams(BaseModel):
    params: List[HyperParam]


class ModelSummary(BaseModel):
    session_id: int
    name: str
    features_cnn_id: int
    optimizer_id: int
    loss_function_id: int
    augmentation: int
    learning_speed: float
    epoch_count: int


class Model(BaseModel):
    id: int
    session_id: int
    name: str
    features_cnn_id: int
    optimizer_id: int
    loss_function_id: int
    augmentation: int
    learning_speed: float
    epoch_count: int


class OptimizerSummary(BaseModel):
    name: str


class Optimizer(BaseModel):
    id: int
    name: str


class UserSession(BaseModel):
    id: int
    dataset_path: str
    data_markup_path: str
    user_id: int


class UserSessionSummary(BaseModel):
    dataset_path: str
    data_markup_path: str
    user_id: int


class User(BaseModel):
    id: int
    name: str
    email: str


def json_to_schema(json_bytes, schema_type: BaseModel.__class__):
    schema = json.loads(json_bytes.decode('utf-8'))
    return parse_obj_as(schema_type, schema)


def json_array_to_schema(json_array, schema_type: BaseModel.__class__):
    items = []
    for row in json_array:
        schema = json.loads(row.decode('utf-8'))
        items.append(parse_obj_as(schema_type, schema))
    return items
