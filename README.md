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

## 快速开始

```bash
# 1. 安装依赖
uv sync --dev

# 2. 环境配置（默认 SQLite，无需修改）
cp .env.example .env

# 3. 数据库迁移
uv run python manage.py migrate

# 4. 启动服务
uv run python manage.py runserver
```

> 📖 更详细的安装指南、数据库切换、常见问题请见 [docs/getting-started.md](./docs/getting-started.md)。

## 访问 API 文档

- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc
- **健康检查**: http://127.0.0.1:8000/api/

## API 接口概览

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

## 项目结构

```
project_root/
├── config/                  # Django 项目配置
├── events/                  # 示例 App（事件管理系统）
├── logs/                    # 日志目录
├── docs/                    # 📖 项目文档
│   ├── getting-started.md   # 详细启动指南
│   ├── architecture.md      # 架构设计说明
│   └── uv-best-practice.md  # uv 使用最佳实践
├── manage.py
├── pyproject.toml           # 项目配置 + 依赖声明
├── uv.lock                  # 依赖锁定文件
├── requirements.txt         # 兼容 pip 的依赖列表
├── .env.example             # 环境变量模板
├── .python-version          # Python 版本锁定
└── README.md
```

> 📖 完整的架构说明请见 [docs/architecture.md](./docs/architecture.md)。

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

## 代码规范

- 所有函数/方法必须包含完整类型注解
- 函数长度不超过 50 行
- 使用 Google 风格 Docstring
- 导入顺序: 标准库 -> 第三方库 -> Django -> 本地应用
