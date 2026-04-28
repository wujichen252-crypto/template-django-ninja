# Django + django-ninja 项目规则

## 项目概述
基于 Django + django-ninja 的 RESTful API 后端模板项目。

---

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Django 3.1+ |
| REST API | django-ninja v1.6.2 |
| 数据验证 | pydantic v2 |
| 数据库 | SQLite（默认）/ Django ORM |
| 测试 | pytest + pytest-django |
| 类型检查 | mypy（严格模式） |
| 代码检查 | ruff |
| 格式化 | ruff formatter |

---

## 代码规范

### 通用约定
- 使用 Python 3.12+ 语法特性
- 所有函数/方法必须包含完整类型注解（`disallow_untyped_defs = True`）
- 函数长度不超过 50 行，超过需拆分
- 禁止使用 `Any` 类型（除非绝对必要）
- 使用 `snake_case` 命名变量、函数和方法
- 使用 `PascalCase` 命名类
- 使用 `UPPER_SNAKE_CASE` 命名常量
- 必须为所有公共函数/方法编写 Google 风格 Docstring

### 导入顺序
按以下分组排序，每组之间空一行：
1. Python 标准库
2. 第三方库（Django、pydantic 等）
3. django-ninja 导入
4. 本地应用导入

```python
import contextlib
from pathlib import Path
from typing import List, Optional

from django.db import models
from django.http import HttpRequest, HttpResponse
from pydantic import BaseModel

from ninja import NinjaAPI, Router, Schema

from .models import Event
```

### API 设计规范
- 使用 `Router` 组织 API 端点，按功能模块拆分
- 通过 `api.add_router()` 挂载子路由
- 路由路径前缀使用小写字母，单词间用连字符（`/api/v1/events/`）
- URL 名称使用 `kebab-case`（如 `url_name="event-create-url-name"`）
- 禁止在 Handler 中编写业务逻辑，调用 Service 层处理

### Schema 设计规范
- 继承 `ninja.Schema` 或 `pydantic.BaseModel`
- ORM 映射必须设置 `model_config = dict(from_attributes=True)`
- 使用 Field 定义字段别名、默认值等
- Resolver 方法命名格式：`resolve_<field_name>`

```python
class EventSchema(BaseModel):
    model_config = dict(from_attributes=True)
    title: str
    start_date: date
    end_date: date
```

### 模型设计规范
- Django Model 必须包含 `__str__` 方法
- 字段定义添加注释说明用途
- 使用 Django 内置字段类型（CharField, DateField 等）
- 关联关系使用 `ForeignKey`、`OneToOneField`、`ManyToManyField`

```python
class Event(models.Model):
    title = models.CharField(max_length=100)
    category = models.OneToOneField(Category, null=True, blank=True, on_delete=models.SET_NULL)
```

### 错误处理规范
- 使用 django-ninja 内置异常：`HttpError`、`ValidationError`、`AuthenticationError`、`AuthorizationError`
- 通过 `api.add_exception_handler()` 注册自定义异常处理器
- 禁止在 Handler 中直接 `try/except` 后返回 Response

```python
from ninja.errors import HttpError

raise HttpError(404, "Event not found")
```

### 测试规范
- 使用 pytest + pytest-django
- 测试文件命名：`test_<module_name>.py`
- 使用 `TestClient` 进行 API 集成测试（来自 `ninja.testing`）
- 测试函数命名：`test_<feature_name>`
- 使用 `@pytest.mark.parametrize` 进行参数化测试

```python
from ninja import NinjaAPI
from ninja.testing import TestClient

client = TestClient(api)

def test_get_events():
    response = client.get("/events")
    assert response.status_code == 200
```

---

## 项目结构

```
project_root/
├── <app_name>/              # Django App 目录
│   ├── __init__.py
│   ├── admin.py
│   ├── api.py              # API 路由和端点定义
│   ├── models.py           # 数据模型
│   ├── schemas.py          # pydantic Schema 定义
│   ├── services.py         # 业务逻辑层
│   ├── views.py
│   └── tests/
│       ├── __init__.py
│       └── test_api.py
├── <project_name>/         # Django 项目配置目录
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py             # 根路由配置
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
└── pyproject.toml          # ruff、mypy 等工具配置
```

---

## 开发命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py migrate

# 运行开发服务器
python manage.py runserver

# 运行测试
pytest

# 代码检查
ruff check .

# 代码格式化
ruff format .

# 类型检查
mypy .
```

---

## Git 工作流

### 分支策略
- `main`：稳定版本，只接受 PR 合并
- `dev`：开发分支
- `feature/<name>`：功能开发分支
- `fix/<name>`：Bug 修复分支

### 提交信息规范
```
<type>(<scope>): <description>

feat:    新功能
fix:     Bug 修复
refactor: 重构
test:    测试相关
docs:    文档相关
chore:   构建/工具相关
style:   代码格式
```

---

## 额外注意事项

- 敏感配置（SECRET_KEY、数据库密码等）使用环境变量，禁止硬编码
- 数据库迁移文件必须经过 `python manage.py makemigrations` 生成
- 每次提交前运行 `ruff check .` 和 `mypy .` 确保代码质量
- API 变更需同步更新文档
- 禁止在代码中保留调试输出（print 语句）
