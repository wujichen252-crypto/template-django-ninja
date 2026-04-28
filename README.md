# Django + django-ninja RESTful API 模板

基于 Django + django-ninja 的 RESTful API 后端模板项目，提供完整的项目结构、分层架构和最佳实践，**克隆即可运行**。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Django 4.2 LTS |
| REST API | django-ninja 1.6.2 |
| 数据验证 | Pydantic v2 |
| 数据库 | SQLite（默认）/ PostgreSQL / MySQL |
| 环境配置 | python-dotenv + dj-database-url |
| 跨域 | django-cors-headers |
| 测试 | pytest + pytest-django |
| 类型检查 | mypy（严格模式） |
| 代码检查 | ruff |
| 包管理 | uv（推荐） |

## 项目结构

```
project_root/
├── config/                  # Django 项目配置
│   ├── __init__.py
│   ├── settings.py          # 项目设置（含 .env 加载、CORS、日志）
│   ├── urls.py              # 根路由（含 API 注册和健康检查）
│   ├── wsgi.py              # WSGI 应用
│   └── asgi.py              # ASGI 应用
├── events/                  # 示例 App（事件管理系统）
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py             # Django Admin
│   ├── models.py            # 数据模型（Category / Event / Attendee）
│   ├── schemas.py           # Pydantic Schema
│   ├── services.py          # 业务逻辑层
│   ├── api.py               # API 路由
│   ├── views.py
│   └── tests/               # 测试目录
│       └── test_api.py
├── logs/                    # 日志目录
├── manage.py
├── pyproject.toml           # 项目配置 + 依赖声明
├── uv.lock                  # 依赖锁定文件
├── requirements.txt         # 兼容 pip 的依赖列表
├── .env.example             # 环境变量模板
├── .python-version          # Python 版本锁定
└── README.md
```

## 快速开始

### 方式一：uv（推荐，极速）

```bash
# 1. 安装依赖（含开发依赖）
uv sync --dev

# 2. 数据库迁移
uv run python manage.py migrate

# 3. 运行开发服务器
uv run python manage.py runserver
```

### 方式二：pip（传统方式）

```bash
# 1. 创建虚拟环境并激活
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 运行开发服务器
python manage.py runserver
```

## 访问 API 文档

- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc
- **健康检查**: http://127.0.0.1:8000/api/

## 环境变量配置

复制 `.env.example` 为 `.env`，按需修改：

```bash
cp .env.example .env
```

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DJANGO_SECRET_KEY` | Django 密钥 | `django-insecure-dev-key-change-in-production` |
| `DJANGO_DEBUG` | 调试模式 | `True` |
| `DJANGO_ALLOWED_HOSTS` | 允许的主机 | `localhost,127.0.0.1` |
| `DATABASE_URL` | 数据库连接 URL | `sqlite:///db.sqlite3` |
| `CORS_ALLOWED_ORIGINS` | 跨域允许来源 | `http://localhost:3000,...` |

### 数据库切换示例

```bash
# SQLite（默认，零配置）
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL
DATABASE_URL=postgres://user:password@localhost:5432/mydb

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/mydb
```

使用 PostgreSQL / MySQL 时，请先安装对应驱动：

```bash
# uv
uv sync --extra db

# pip
pip install psycopg2-binary  # PostgreSQL
pip install mysqlclient      # MySQL
```

## 开发命令

```bash
# 运行测试
uv run pytest

# 代码检查
uv run ruff check .

# 代码格式化
uv run ruff format .

# 类型检查
uv run mypy .
```

## API 接口

### 健康检查

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/` | 服务健康检查 |

### 分类接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/events/categories` | 获取分类列表 |
| POST | `/api/events/categories` | 创建分类 |
| GET | `/api/events/categories/{id}` | 获取分类详情 |
| PUT | `/api/events/categories/{id}` | 更新分类 |
| DELETE | `/api/events/categories/{id}` | 删除分类 |

### 事件接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/events/events` | 获取事件列表（支持分页、upcoming_only 筛选） |
| POST | `/api/events/events` | 创建事件 |
| GET | `/api/events/events/{id}` | 获取事件详情 |
| PUT | `/api/events/events/{id}` | 更新事件 |
| DELETE | `/api/events/events/{id}` | 删除事件 |
| GET | `/api/events/events/{id}/attendees` | 获取参与者列表 |
| POST | `/api/events/events/{id}/attendees` | 添加参与者 |
| DELETE | `/api/events/attendees/{id}` | 删除参与者 |

## 架构设计

### 分层结构

```
Handler (api.py) -> Service (services.py) -> Repository (models.py)
```

- **api.py**: 定义 API 路由，处理请求/响应，调用 Service 层
- **services.py**: 封装业务逻辑、数据验证、事务管理
- **models.py**: 定义数据模型，Django ORM 操作

### 安全认证配置

API 文档已预配置两种安全方案：
- **Bearer Token** (`Authorization: Bearer <JWT>`)
- **API Key** (`X-API-Key: <key>`)

需在具体接口上使用 `@router.get(..., auth=...)` 开启认证。

## 代码规范

- 所有函数/方法必须包含完整类型注解
- 函数长度不超过 50 行
- 使用 Google 风格 Docstring
- 导入顺序: 标准库 -> 第三方库 -> Django -> 本地应用
