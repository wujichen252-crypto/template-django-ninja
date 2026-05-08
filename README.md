# Django + django-ninja RESTful API 模板

基于 Django + django-ninja 的 RESTful API 后端模板项目，提供完整的项目结构、分层架构和最佳实践，**克隆即可运行**。

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Django 3.2 LTS |
| REST API | django-ninja 1.3.0 |
| 数据验证 | Pydantic v2 |
| 数据库 | SQLite（默认）/ PostgreSQL / MySQL |
| 环境配置 | python-dotenv + dj-database-url |
| 跨域 | django-cors-headers |
| 测试 | pytest + pytest-django |
| 类型检查 | mypy（严格模式） |
| 代码检查 | ruff |
| 包管理 | uv |

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

## 项目结构

```
project_root/
├── api/                      # 主应用模块
│   ├── __init__.py
│   ├── api.py              # API 路由定义
│   ├── apps.py             # 应用配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic Schema
│   ├── services.py         # 业务逻辑层
│   ├── views.py            # 视图层
│   └── tests/              # 测试目录
├── config/                  # Django 项目配置
├── logs/                    # 日志目录
├── docs/                    # 📖 项目文档
│   ├── getting-started.md   # 详细启动指南
│   ├── architecture.md     # 架构设计说明
│   └── uv-best-practice.md  # uv 使用最佳实践
├── manage.py
├── pyproject.toml           # 项目配置 + 依赖声明
├── uv.lock                  # 依赖锁定文件
├── .env.example             # 环境变量模板
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
