"""Events 数据模型定义."""
from django.db import models


class Category(models.Model):
    """事件分类模型."""

    name = models.CharField(max_length=50, verbose_name="分类名称")
    description = models.TextField(blank=True, verbose_name="分类描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类列表"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    """事件模型."""

    title = models.CharField(max_length=100, verbose_name="事件标题")
    description = models.TextField(blank=True, verbose_name="事件描述")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
        verbose_name="分类",
    )
    location = models.CharField(max_length=200, blank=True, verbose_name="地点")
    max_attendees = models.PositiveIntegerField(default=0, verbose_name="最大参与人数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件列表"
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["start_date"]),
            models.Index(fields=["category", "start_date"]),
        ]

    def __str__(self) -> str:
        return self.title


class Attendee(models.Model):
    """事件参与者模型."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attendees",
        verbose_name="关联事件",
    )
    name = models.CharField(max_length=50, verbose_name="参与者姓名")
    email = models.EmailField(verbose_name="电子邮件")
    phone = models.CharField(max_length=20, blank=True, verbose_name="电话号码")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="报名时间")
    notes = models.TextField(blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "参与者"
        verbose_name_plural = "参与者列表"
        ordering = ["-registration_date"]
        unique_together = ["event", "email"]

    def __str__(self) -> str:
        return f"{self.name} - {self.event.title}"
