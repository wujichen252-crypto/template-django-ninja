"""Pydantic Schema 定义.

展示 django-ninja + Pydantic v2 的最佳实践：
- Field 验证（min_length, gt, examples）
- 泛型分页响应
- 统一错误响应格式
"""

from datetime import datetime
from decimal import Decimal
from typing import Literal

from ninja import Schema
from pydantic import Field, field_validator


class MessageResponse(Schema):
    """通用消息响应."""

    message: str


class ErrorResponse(Schema):
    """统一错误响应格式."""

    detail: str
    code: str = "error"


# ─── Item Schemas ────────────────────────────────────────────────


class ItemCreate(Schema):
    """创建商品请求."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["全新笔记本电脑"],
        description="商品标题",
    )
    description: str = Field(
        "",
        max_length=2000,
        examples=["2024 年款，16GB 内存，512GB 固态硬盘"],
        description="商品描述",
    )
    price: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        examples=[5999.00],
        description="商品价格",
    )
    status: Literal["draft", "published", "archived"] = Field(
        "draft",
        description="商品状态",
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        """标题不能仅含空白字符."""
        if v.strip() == "":
            msg = "标题不能仅含空白字符"
            raise ValueError(msg)
        return v.strip()


class ItemUpdate(Schema):
    """更新商品请求（全部可选，仅更新提供字段）."""

    title: str | None = Field(
        None,
        min_length=1,
        max_length=200,
        description="商品标题",
    )
    description: str | None = Field(
        None,
        max_length=2000,
        description="商品描述",
    )
    price: Decimal | None = Field(
        None,
        gt=0,
        decimal_places=2,
        description="商品价格",
    )
    status: Literal["draft", "published", "archived"] | None = Field(
        None,
        description="商品状态",
    )


class ItemResponse(Schema):
    """商品响应."""

    id: int
    title: str
    description: str
    price: Decimal
    status: str
    created_at: datetime
    updated_at: datetime


# ─── Pagination ──────────────────────────────────────────────────


class PaginatedResponse[T](Schema):
    """泛型分页响应."""

    items: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int
