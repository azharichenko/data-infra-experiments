from typing import TypeVar

from common.base import BaseIntegration, BaseDataProvider
from common.models import BaseModel

Integration = TypeVar("Integration", bound=BaseIntegration)
DataProvider = TypeVar("DataProvider", bound="BaseDataProvider")
Model = TypeVar("Model", bound="BaseModel")
