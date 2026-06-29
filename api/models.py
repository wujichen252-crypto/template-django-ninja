"""API 数据模型定义.

包含基础 Mixin 类和示例业务模型，展示 Django 最佳实践。
"""

from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    """时间戳 Mixin: 自动记录创建和更新时间."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """软删除 Mixin: 标记删除而非物理删除."""

    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="删除时间")

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """标记为已删除."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def restore(self) -> None:
        """恢复已删除的记录."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])


class ItemStatus(models.TextChoices):
    """商品状态枚举."""

    DRAFT = "draft", _("草稿")
    PUBLISHED = "published", _("已发布")
    ARCHIVED = "archived", _("已归档")


class Item(TimestampMixin, SoftDeleteMixin):
    """示例商品模型.

    展示 Django ORM 最佳实践：
    - Mixin 继承（时间戳、软删除）
    - TextChoices 枚举
    - 显式 Meta 配置
    - 复合索引
    """

    title = models.CharField(max_length=200, verbose_name="标题")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="价格",
    )
    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.DRAFT,
        verbose_name="状态",
    )

    class Meta:
        db_table = "api_item"
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status", "created_at"], name="idx_item_status_created"
            ),
            models.Index(
                fields=["is_deleted", "created_at"], name="idx_item_deleted_created"
            ),
        ]

    def __str__(self) -> str:
        return self.title
