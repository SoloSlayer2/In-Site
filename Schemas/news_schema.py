from typing import List, Optional

from pydantic import BaseModel


class NewsSummaryRequest(BaseModel):
    query: str


class FactCheckRequest(BaseModel):
    news: str
