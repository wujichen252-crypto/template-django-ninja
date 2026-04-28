"""Events API 路由定义."""
from typing import Any

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from .schemas import (
    AttendeeCreateSchema,
    AttendeeSchema,
    CategoryCreateSchema,
    CategorySchema,
    EventCreateSchema,
    EventSchema,
    EventUpdateSchema,
    PaginatedEventResponse,
)
from .services import AttendeeService, CategoryService, EventService

router = Router(tags=["Events"])


@router.get("/categories", response=list[CategorySchema])
def list_categories(request: HttpRequest) -> list[CategorySchema]:
    """获取所有分类列表."""
    categories = CategoryService.get_all_categories()
    return list(categories)  # type: ignore[arg-type]


@router.post("/categories", response=CategorySchema, url_name="category-create")
def create_category(
    request: HttpRequest, payload: CategoryCreateSchema
) -> CategorySchema:
    """创建新分类."""
    category = CategoryService.create_category(
        name=payload.name,
        description=payload.description,
    )
    return category  # type: ignore[return-value]


@router.get("/categories/{category_id}", response=CategorySchema)
def get_category(request: HttpRequest, category_id: int) -> CategorySchema:
    """获取指定分类详情."""
    category = CategoryService.get_category_by_id(category_id)
    if category is None:
        raise HttpError(404, "分类不存在")
    return category  # type: ignore[return-value]


@router.put("/categories/{category_id}", response=CategorySchema)
def update_category(
    request: HttpRequest, category_id: int, payload: CategoryCreateSchema
) -> CategorySchema:
    """更新指定分类."""
    category = CategoryService.update_category(
        category_id=category_id,
        name=payload.name,
        description=payload.description,
    )
    if category is None:
        raise HttpError(404, "分类不存在")
    return category  # type: ignore[return-value]


@router.delete("/categories/{category_id}")
def delete_category(request: HttpRequest, category_id: int) -> dict[str, Any]:
    """删除指定分类."""
    success = CategoryService.delete_category(category_id)
    if not success:
        raise HttpError(404, "分类不存在")
    return {"success": True, "message": "分类已删除"}


@router.get("/events", response=PaginatedEventResponse, url_name="event-list")
def list_events(
    request: HttpRequest,
    page: int = 1,
    page_size: int = 10,
    upcoming_only: bool = False,
) -> PaginatedEventResponse:
    """获取事件列表（支持分页和筛选）."""
    events = (
        EventService.get_upcoming_events()
        if upcoming_only
        else EventService.get_all_events()
    )
    total = events.count()
    start = (page - 1) * page_size
    end = start + page_size
    paginated_events = list(events[start:end])
    return PaginatedEventResponse(
        total=total,
        page=page,
        page_size=page_size,
        events=paginated_events,  # type: ignore[arg-type]
    )


@router.post("/events", response=EventSchema, url_name="event-create")
def create_event(
    request: HttpRequest, payload: EventCreateSchema
) -> EventSchema:
    """创建新事件."""
    if payload.start_date > payload.end_date:
        raise HttpError(400, "开始日期不能晚于结束日期")
    if payload.category_id:
        category = CategoryService.get_category_by_id(payload.category_id)
        if category is None:
            raise HttpError(400, "指定的分类不存在")
    event = EventService.create_event(
        title=payload.title,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
        category_id=payload.category_id,
        location=payload.location,
        max_attendees=payload.max_attendees,
    )
    return event  # type: ignore[return-value]


@router.get("/events/{event_id}", response=EventSchema)
def get_event(request: HttpRequest, event_id: int) -> EventSchema:
    """获取指定事件详情."""
    event = EventService.get_event_by_id(event_id)
    if event is None:
        raise HttpError(404, "事件不存在")
    return event  # type: ignore[return-value]


@router.put("/events/{event_id}", response=EventSchema)
def update_event(
    request: HttpRequest, event_id: int, payload: EventUpdateSchema
) -> EventSchema:
    """更新指定事件."""
    if payload.start_date and payload.end_date:
        if payload.start_date > payload.end_date:
            raise HttpError(400, "开始日期不能晚于结束日期")
    event = EventService.update_event(
        event_id=event_id,
        title=payload.title,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
        category_id=payload.category_id,
        location=payload.location,
        max_attendees=payload.max_attendees,
    )
    if event is None:
        raise HttpError(404, "事件不存在")
    return event  # type: ignore[return-value]


@router.delete("/events/{event_id}")
def delete_event(request: HttpRequest, event_id: int) -> dict[str, Any]:
    """删除指定事件."""
    success = EventService.delete_event(event_id)
    if not success:
        raise HttpError(404, "事件不存在")
    return {"success": True, "message": "事件已删除"}


@router.get("/events/{event_id}/attendees", response=list[AttendeeSchema])
def list_event_attendees(
    request: HttpRequest, event_id: int
) -> list[AttendeeSchema]:
    """获取事件的参与者列表."""
    event = EventService.get_event_by_id(event_id)
    if event is None:
        raise HttpError(404, "事件不存在")
    return list(AttendeeService.get_attendees_by_event(event_id))  # type: ignore[arg-type]


@router.post("/events/{event_id}/attendees", response=AttendeeSchema)
def create_attendee(
    request: HttpRequest, event_id: int, payload: AttendeeCreateSchema
) -> AttendeeSchema:
    """为事件添加参与者."""
    attendee = AttendeeService.create_attendee(
        event_id=event_id,
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        notes=payload.notes,
    )
    if attendee is None:
        raise HttpError(400, "创建参与者失败，可能事件不存在或参与人数已满")
    return attendee  # type: ignore[return-value]


@router.delete("/attendees/{attendee_id}")
def delete_attendee(request: HttpRequest, attendee_id: int) -> dict[str, Any]:
    """删除参与者."""
    success = AttendeeService.delete_attendee(attendee_id)
    if not success:
        raise HttpError(404, "参与者不存在")
    return {"success": True, "message": "参与者已删除"}
