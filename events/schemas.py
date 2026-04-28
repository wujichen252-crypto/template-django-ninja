"""Events Pydantic Schema 定义."""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategorySchema(BaseModel):
    """分类 Schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str = ""
    created_at: datetime
    updated_at: datetime


class CategoryCreateSchema(BaseModel):
    """创建分类请求 Schema."""

    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    description: str = Field(default="", description="分类描述")


class EventSchema(BaseModel):
    """事件 Schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str = ""
    start_date: date
    end_date: date
    category: CategorySchema | None = None
    location: str = ""
    max_attendees: int = 0
    created_at: datetime
    updated_at: datetime


class EventCreateSchema(BaseModel):
    """创建事件请求 Schema."""

    title: str = Field(..., min_length=1, max_length=100, description="事件标题")
    description: str = Field(default="", description="事件描述")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    category_id: int | None = Field(None, description="分类ID")
    location: str = Field(default="", max_length=200, description="地点")
    max_attendees: int = Field(default=0, ge=0, description="最大参与人数")


class EventUpdateSchema(BaseModel):
    """更新事件请求 Schema."""

    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    category_id: int | None = None
    location: str | None = Field(None, max_length=200)
    max_attendees: int | None = Field(None, ge=0)


class AttendeeSchema(BaseModel):
    """参与者 Schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    name: str
    email: EmailStr
    phone: str = ""
    registration_date: datetime
    notes: str = ""


class AttendeeCreateSchema(BaseModel):
    """创建参与者请求 Schema."""

    name: str = Field(..., min_length=1, max_length=50, description="参与者姓名")
    email: EmailStr = Field(..., description="电子邮件")
    phone: str = Field(default="", max_length=20, description="电话号码")
    notes: str = Field(default="", description="备注")


class EventListResponse(BaseModel):
    """事件列表响应 Schema."""

    total: int
    events: list[EventSchema]


class PaginatedEventResponse(BaseModel):
    """分页事件响应 Schema."""

    total: int
    page: int
    page_size: int
    events: list[EventSchema]
