"""Events 业务逻辑层服务."""
from typing import Optional

from django.db.models import QuerySet

from .models import Attendee, Category, Event


class CategoryService:
    """分类服务层."""

    @staticmethod
    def get_all_categories() -> QuerySet[Category]:
        """获取所有分类."""
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(category_id: int) -> Optional[Category]:
        """根据ID获取分类."""
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    @staticmethod
    def create_category(name: str, description: str = "") -> Category:
        """创建新分类."""
        return Category.objects.create(name=name, description=description)

    @staticmethod
    def update_category(
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Category]:
        """更新分类."""
        category = CategoryService.get_category_by_id(category_id)
        if category is None:
            return None
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description
        category.save()
        return category

    @staticmethod
    def delete_category(category_id: int) -> bool:
        """删除分类."""
        category = CategoryService.get_category_by_id(category_id)
        if category is None:
            return False
        category.delete()
        return True


class EventService:
    """事件服务层."""

    @staticmethod
    def get_all_events() -> QuerySet[Event]:
        """获取所有事件."""
        return Event.objects.select_related("category").all()

    @staticmethod
    def get_upcoming_events() -> QuerySet[Event]:
        """获取即将到来的事件."""
        from datetime import date

        return Event.objects.select_related("category").filter(
            start_date__gte=date.today()
        )

    @staticmethod
    def get_event_by_id(event_id: int) -> Optional[Event]:
        """根据ID获取事件."""
        try:
            return Event.objects.select_related("category").get(id=event_id)
        except Event.DoesNotExist:
            return None

    @staticmethod
    def create_event(
        title: str,
        start_date,
        end_date,
        description: str = "",
        category_id: Optional[int] = None,
        location: str = "",
        max_attendees: int = 0,
    ) -> Event:
        """创建新事件."""
        category = None
        if category_id:
            category = CategoryService.get_category_by_id(category_id)
        return Event.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            category=category,
            location=location,
            max_attendees=max_attendees,
        )

    @staticmethod
    def update_event(
        event_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        start_date=None,
        end_date=None,
        category_id: Optional[int] = None,
        location: Optional[str] = None,
        max_attendees: Optional[int] = None,
    ) -> Optional[Event]:
        """更新事件."""
        event = EventService.get_event_by_id(event_id)
        if event is None:
            return None
        if title is not None:
            event.title = title
        if description is not None:
            event.description = description
        if start_date is not None:
            event.start_date = start_date
        if end_date is not None:
            event.end_date = end_date
        if category_id is not None:
            event.category = CategoryService.get_category_by_id(category_id)
        if location is not None:
            event.location = location
        if max_attendees is not None:
            event.max_attendees = max_attendees
        event.save()
        return event

    @staticmethod
    def delete_event(event_id: int) -> bool:
        """删除事件."""
        event = EventService.get_event_by_id(event_id)
        if event is None:
            return False
        event.delete()
        return True

    @staticmethod
    def get_events_by_category(category_id: int) -> QuerySet[Event]:
        """根据分类获取事件."""
        return Event.objects.select_related("category").filter(category_id=category_id)

    @staticmethod
    def search_events(keyword: str) -> QuerySet[Event]:
        """搜索事件."""
        return Event.objects.select_related("category").filter(
            title__icontains=keyword
        ) | Event.objects.select_related("category").filter(
            description__icontains=keyword
        )


class AttendeeService:
    """参与者服务层."""

    @staticmethod
    def get_attendees_by_event(event_id: int) -> QuerySet[Attendee]:
        """获取事件的参与者."""
        return Attendee.objects.filter(event_id=event_id)

    @staticmethod
    def get_attendee_by_id(attendee_id: int) -> Optional[Attendee]:
        """根据ID获取参与者."""
        try:
            return Attendee.objects.get(id=attendee_id)
        except Attendee.DoesNotExist:
            return None

    @staticmethod
    def create_attendee(
        event_id: int,
        name: str,
        email: str,
        phone: str = "",
        notes: str = "",
    ) -> Optional[Attendee]:
        """创建参与者."""
        event = EventService.get_event_by_id(event_id)
        if event is None:
            return None
        if event.max_attendees > 0:
            current_count = Attendee.objects.filter(event_id=event_id).count()
            if current_count >= event.max_attendees:
                return None
        return Attendee.objects.create(
            event=event,
            name=name,
            email=email,
            phone=phone,
            notes=notes,
        )

    @staticmethod
    def delete_attendee(attendee_id: int) -> bool:
        """删除参与者."""
        attendee = AttendeeService.get_attendee_by_id(attendee_id)
        if attendee is None:
            return False
        attendee.delete()
        return True

    @staticmethod
    def get_attendee_count(event_id: int) -> int:
        """获取事件的参与者数量."""
        return Attendee.objects.filter(event_id=event_id).count()
