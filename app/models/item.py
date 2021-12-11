from pydantic import BaseModel
from typing import List, Optional


class Item(BaseModel):
    id: int
    by: Optional[str]
    descendants: Optional[int]
    kids: Optional[List[int]]
    score: Optional[int]
    time: Optional[int]
    title: Optional[str]
    type: Optional[str]
    url: Optional[str]
    deleted: Optional[bool]
    text: Optional[str]
    dead: Optional[str]
    parent: Optional[int]
    poll: Optional[int]
    parts: Optional[List[int]]