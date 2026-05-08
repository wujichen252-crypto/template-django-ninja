"""API Schema 定义."""
from ninja import Schema


class MessageSchema(Schema):
    """通用消息响应."""

    message: str
