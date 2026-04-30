# 快速开始

本文档将指导你从零开始启动本项目。

## 环境要求

| 项目 | 版本 |
|------|------|
| Python | >= 3.12 |
| 包管理器 | uv |

> 项目根目录的 `.python-version` 文件已锁定 Python 版本为 `3.12`，建议使用 [pyenv](https://github.com/pyenv/pyenv) 或 uv 管理 Python 版本。

## 使用 uv

### 1. 安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 同步依赖

```bash
# 安装生产依赖 + 开发依赖
uv sync --dev

# 如需使用 PostgreSQL / MySQL，额外安装数据库驱动
uv sync --dev --extra db
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

默认使用 SQLite，无需修改即可运行。如需切换数据库，请编辑 `.env` 中的 `DATABASE_URL`。

### 4. 数据库迁移

```bash
uv run python manage.py migrate
```

### 5. 启动开发服务器

```bash
uv run python manage.py runserver
```

访问 http://127.0.0.1:8000/api/docs 查看 Swagger 文档。


## 开发常用命令

```bash
# 运行测试
uv run pytest

# 代码风格检查
uv run ruff check .

# 自动格式化
uv run ruff format .

# 类型检查
uv run mypy .
```

## 常见问题

### Q: Windows 下 `uv run` 提示权限错误？

以管理员身份运行 PowerShell，执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: `migrate` 后没有表创建？

请确认 `events/migrations/` 目录下的迁移文件存在。如果缺失，可尝试：

```bash
uv run python manage.py makemigrations events
uv run python manage.py migrate
```

### Q: 如何切换数据库？

修改 `.env` 中的 `DATABASE_URL`：

```bash
# SQLite（默认）
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/dbname
```

使用 PostgreSQL / MySQL 前，请先安装对应驱动：

```bash
uv sync --extra db
```
