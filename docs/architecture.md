# 架构设计

## 分层结构

本项目采用经典的三层架构，职责清晰、易于测试和扩展：

```
┌─────────────────────────────────────┐
│           API 层 (api.py)            │  ← 路由定义、参数校验、响应序列化
│         Router → NinjaAPI            │
├─────────────────────────────────────┤
│         Service 层 (services.py)     │  ← 业务逻辑、数据校验、事务控制
├─────────────────────────────────────┤
│         Model 层 (models.py)         │  ← Django ORM、数据持久化
└─────────────────────────────────────┘
```

### 各层职责

| 层级 | 文件 | 职责 | 禁止做的事 |
|------|------|------|-----------|
| API | `api.py` | 定义路由、接收请求、调用 Service、返回响应 | 直接操作 ORM |
| Service | `services.py` | 实现业务规则、数据组装、异常处理 | 处理 HTTP 请求/响应 |
| Model | `models.py` | 定义数据结构、建立关联、配置 Meta | 编写业务逻辑 |

## 请求生命周期

```
Client Request
    ↓
NinjaAPI Router (路由匹配 + 参数反序列化)
    ↓
Schema Validation (Pydantic 自动校验)
    ↓
api.py Handler (调用 Service)
    ↓
services.py (业务逻辑 + ORM 操作)
    ↓
models.py (数据库读写)
    ↓
Response Serialization (Schema → JSON)
    ↓
Client Response
```

## 技术选型说明

### 为什么用 django-ninja？

- **类型驱动**：基于 Python 类型注解，自动生成 OpenAPI 文档
- **性能**：比 Django REST Framework 更快，路由解析更高效
- **Pydantic v2**：享受最新的数据验证和序列化能力

### 为什么分离 Service 层？

- **可测试**：业务逻辑不依赖 HTTP 上下文，单元测试更简单
- **可复用**：Service 方法可在 Admin 命令、Celery 任务中复用
- **可维护**：业务变更集中在 Service，不影响接口契约

## 模块划分

```
api/                        # 主应用模块
├── __init__.py
├── api.py                 # API 路由定义
├── apps.py                # 应用配置
├── models.py              # 数据模型
├── schemas.py             # Pydantic 请求/响应模型
├── services.py            # 业务逻辑
├── views.py               # 视图层（备用）
└── tests/
    └── test_api.py        # 接口测试
```

新增业务模块时，可按上述结构扩展 `api/` 目录下的文件。

## 安全设计

### 认证方案

项目在 `config/urls.py` 中预配置了两套安全方案：

1. **Bearer Token**（JWT）
   ```
   Authorization: Bearer <token>
   ```

2. **API Key**
   ```
   X-API-Key: <key>
   ```

> 实际开启认证需在接口装饰器上添加 `auth` 参数，例如：
> ```python
> @router.get("/items", auth=AuthBearer())
> ```

### CORS 策略

默认仅允许常见前端开发端口跨域访问：

```
http://localhost:3000      # Next.js / React 默认
http://localhost:5173      # Vite 默认
```

生产环境请通过 `.env` 的 `CORS_ALLOWED_ORIGINS` 精确配置允许的来源。

## 日志策略

| 环境 | 输出目标 | 级别 |
|------|---------|------|
| DEBUG=True | 控制台 | INFO |
| DEBUG=False | 控制台 + 文件 | INFO |
| api 模块 | 控制台 + 文件 | DEBUG/INFO |

日志文件位于 `logs/django.log`，按 5MB 自动轮询，保留 5 个备份。
