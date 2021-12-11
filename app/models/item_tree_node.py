from pydantic import BaseModel
from .item import Item

class ItemTreeNode(BaseModel):
    item: Item
    depth: int