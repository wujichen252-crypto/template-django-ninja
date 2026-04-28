# Django + django-ninja RESTful API 模板

基于 Django + django-ninja 的 RESTful API 后端模板项目，提供完整的项目结构和最佳实践。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Django 4.2+ |
| REST API | django-ninja v1.6.2 |
| 数据验证 | pydantic v2 |
| 数据库 | SQLite（默认）/ Django ORM |
| 测试 | pytest + pytest-django |
| 类型检查 | mypy（严格模式） |
| 代码检查 | ruff |
| 格式化 | ruff formatter |

## 项目结构

```
project_root/
├── config/                  # Django 项目配置
│   ├── __init__.py
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 根路由
│   ├── wsgi.py              # WSGI 应用
│   └── asgi.py              # ASGI 应用
├── events/                  # 示例 App
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py             # Django Admin
│   ├── models.py            # 数据模型
│   ├── schemas.py           # Pydantic Schema
│   ├── services.py          # 业务逻辑层
│   ├── api.py               # API 路由
│   ├── views.py
│   └── tests/               # 测试目录
│       └── test_api.py
├── manage.py
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py migrate
```

### 3. 运行开发服务器

```bash
python manage.py runserver
```

### 4. 访问 API 文档

- Swagger UI: http://127.0.0.1:8000/api/docs
- ReDoc: http://127.0.0.1:8000/api/redoc

## 开发命令

```bash
# 运行测试
pytest

# 代码检查
ruff check .

# 代码格式化
ruff format .

# 类型检查
mypy .
```

## API 接口

### 分类接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/events/categories | 获取分类列表 |
| POST | /api/events/categories | 创建分类 |
| GET | /api/events/categories/{id} | 获取分类详情 |
| PUT | /api/events/categories/{id} | 更新分类 |
| DELETE | /api/events/categories/{id} | 删除分类 |

### 事件接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/events/events | 获取事件列表 |
| POST | /api/events/events | 创建事件 |
| GET | /api/events/events/{id} | 获取事件详情 |
| PUT | /api/events/events/{id} | 更新事件 |
| DELETE | /api/events/events/{id} | 删除事件 |
| GET | /api/events/events/{id}/attendees | 获取参与者列表 |
| POST | /api/events/events/{id}/attendees | 添加参与者 |
| DELETE | /api/events/attendees/{id} | 删除参与者 |

## 架构设计

### 分层结构

```
Handler (api.py) -> Service (services.py) -> Repository (models.py)
```

- **api.py**: 定义 API 路由，处理请求/响应，使用 Service 层处理业务逻辑
- **services.py**: 封装业务逻辑，数据验证，事务管理
- **models.py**: 定义数据模型，Django ORM 操作

### Schema 设计

- **Schema**: Pydantic 模型，用于 API 请求/响应验证
- `from_attributes = True`: 支持 ORM 模型自动转换

## 代码规范

- 所有函数/方法必须包含完整类型注解
- 函数长度不超过 50 行
- 使用 Google 风格 Docstring
- 导入顺序: 标准库 -> 第三方库 -> django-ninja -> 本地应用
