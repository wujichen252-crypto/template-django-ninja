"""Events API 测试."""
from datetime import date, timedelta
from typing import ClassVar

from django.test import TestCase
from ninja import NinjaAPI
from ninja.testing import TestClient

from events.api import router
from events.models import Attendee, Category, Event

api = NinjaAPI()
api.add_router("/events", router)
client = TestClient(api)


class CategoryAPITest(TestCase):
    """分类 API 测试."""

    category: ClassVar[Category]

    @classmethod
    def setUpTestData(cls) -> None:
        """设置测试数据."""
        cls.category = Category.objects.create(
            name="技术会议",
            description="技术相关会议",
        )

    def test_list_categories(self) -> None:
        """测试获取分类列表."""
        response = client.get("/events/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "技术会议"

    def test_create_category(self) -> None:
        """测试创建分类."""
        response = client.post(
            "/events/categories",
            json={"name": "新分类", "description": "测试描述"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "新分类"
        assert Category.objects.count() == 2

    def test_get_category(self) -> None:
        """测试获取单个分类."""
        response = client.get(f"/events/categories/{self.category.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "技术会议"

    def test_get_category_not_found(self) -> None:
        """测试获取不存在的分类."""
        response = client.get("/events/categories/9999")
        assert response.status_code == 404

    def test_update_category(self) -> None:
        """测试更新分类."""
        response = client.put(
            f"/events/categories/{self.category.id}",
            json={"name": "更新后的分类", "description": "更新描述"},
        )
        assert response.status_code == 200
        self.category.refresh_from_db()
        assert self.category.name == "更新后的分类"

    def test_delete_category(self) -> None:
        """测试删除分类."""
        response = client.delete(f"/events/categories/{self.category.id}")
        assert response.status_code == 200
        assert Category.objects.count() == 0


class EventAPITest(TestCase):
    """事件 API 测试."""

    category: ClassVar[Category]
    event: ClassVar[Event]

    @classmethod
    def setUpTestData(cls) -> None:
        """设置测试数据."""
        cls.category = Category.objects.create(name="技术会议")
        cls.event = Event.objects.create(
            title="Django 大会",
            description="Django 年度大会",
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=9),
            category=cls.category,
            location="北京",
            max_attendees=100,
        )

    def test_list_events(self) -> None:
        """测试获取事件列表."""
        response = client.get("/events/events")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["events"]) == 1

    def test_list_events_pagination(self) -> None:
        """测试事件分页."""
        response = client.get("/events/events?page=1&page_size=5")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 5

    def test_create_event(self) -> None:
        """测试创建事件."""
        response = client.post(
            "/events/events",
            json={
                "title": "Python 大会",
                "description": "Python 年度大会",
                "start_date": str(date.today() + timedelta(days=14)),
                "end_date": str(date.today() + timedelta(days=16)),
                "category_id": self.category.id,
                "location": "上海",
                "max_attendees": 200,
            },
        )
        assert response.status_code == 200
        assert Event.objects.count() == 2

    def test_create_event_invalid_dates(self) -> None:
        """测试创建事件（日期无效）."""
        response = client.post(
            "/events/events",
            json={
                "title": "无效日期事件",
                "start_date": str(date.today() + timedelta(days=10)),
                "end_date": str(date.today() + timedelta(days=5)),
            },
        )
        assert response.status_code == 400

    def test_get_event(self) -> None:
        """测试获取单个事件."""
        response = client.get(f"/events/events/{self.event.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Django 大会"

    def test_update_event(self) -> None:
        """测试更新事件."""
        response = client.put(
            f"/events/events/{self.event.id}",
            json={"title": "更新后的大会", "location": "深圳"},
        )
        assert response.status_code == 200
        self.event.refresh_from_db()
        assert self.event.title == "更新后的大会"
        assert self.event.location == "深圳"

    def test_delete_event(self) -> None:
        """测试删除事件."""
        response = client.delete(f"/events/events/{self.event.id}")
        assert response.status_code == 200
        assert Event.objects.count() == 0


class AttendeeAPITest(TestCase):
    """参与者 API 测试."""

    event: ClassVar[Event]
    attendee: ClassVar[Attendee]

    @classmethod
    def setUpTestData(cls) -> None:
        """设置测试数据."""
        cls.event = Event.objects.create(
            title="测试事件",
            start_date=date.today() + timedelta(days=7),
            end_date=date.today() + timedelta(days=9),
            max_attendees=2,
        )
        cls.attendee = Attendee.objects.create(
            event=cls.event,
            name="张三",
            email="zhangsan@example.com",
        )

    def test_list_attendees(self) -> None:
        """测试获取参与者列表."""
        response = client.get(f"/events/events/{self.event.id}/attendees")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_create_attendee(self) -> None:
        """测试创建参与者."""
        response = client.post(
            f"/events/events/{self.event.id}/attendees",
            json={
                "name": "李四",
                "email": "lisi@example.com",
                "phone": "13800138000",
            },
        )
        assert response.status_code == 200
        assert Attendee.objects.count() == 2

    def test_create_attendee_event_full(self) -> None:
        """测试创建参与者（事件已满）."""
        response = client.post(
            f"/events/events/{self.event.id}/attendees",
            json={
                "name": "王五",
                "email": "wangwu@example.com",
            },
        )
        response = client.post(
            f"/events/events/{self.event.id}/attendees",
            json={
                "name": "赵六",
                "email": "zhaoliu@example.com",
            },
        )
        assert response.status_code == 400

    def test_delete_attendee(self) -> None:
        """测试删除参与者."""
        response = client.delete(f"/events/attendees/{self.attendee.id}")
        assert response.status_code == 200
        assert Attendee.objects.count() == 0
