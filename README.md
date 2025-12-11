# 通讯录 Web 应用

## 项目简介

本项目是一个基于 Flask + Vue 3 的通讯录管理系统，实现了用户认证、联系人管理、收藏功能以及 Excel 导入导出等功能。

## 功能特性

- 用户注册与登录（基于 JWT 认证）
- 联系人的增删改查
- 联系人收藏功能
- 支持多种联系方式（电话、邮箱、地址、社交媒体）
- Excel 文件导入导出

## 技术栈

**后端**
- Flask 3.0.0
- Flask-SQLAlchemy（ORM）
- Flask-JWT-Extended（认证）
- MySQL 数据库
- openpyxl（Excel 处理）

**前端**
- Vue 3.5
- Vite（构建工具）
- Element Plus（UI 组件库）
- Pinia（状态管理）
- Axios（HTTP 请求）

## 项目结构

```
极限编程/
├── backend/                    # 后端目录
│   └── backend/
│       ├── app/
│       │   ├── __init__.py     # Flask 应用初始化
│       │   ├── models.py       # 数据库模型
│       │   ├── routes/         # API 路由
│       │   │   ├── auth.py     # 用户认证接口
│       │   │   ├── contacts.py # 联系人接口
│       │   │   └── import_export.py
│       │   └── utils/
│       ├── config.py
│       ├── requirements.txt
│       └── run.py
│
├── frontend/                   # 前端目录
│   ├── src/
│   │   ├── api/                # API 封装
│   │   ├── components/         # 组件
│   │   ├── views/              # 页面
│   │   ├── router/             # 路由
│   │   ├── stores/             # 状态管理
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 环境要求

- Python >= 3.8
- Node.js >= 18
- MySQL >= 5.7

## 安装与运行

### 后端

```bash
cd backend/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库连接

# 运行
python run.py
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

### 数据库

```sql
CREATE DATABASE addressbook CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## API 接口

### 用户认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/logout | 用户登出 |
| GET | /api/auth/me | 获取当前用户 |

### 联系人管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/contacts | 获取联系人列表 |
| POST | /api/contacts | 创建联系人 |
| GET | /api/contacts/:id | 获取单个联系人 |
| PUT | /api/contacts/:id | 更新联系人 |
| DELETE | /api/contacts/:id | 删除联系人 |
| POST | /api/contacts/:id/favorite | 切换收藏状态 |

### 导入导出

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/export | 导出 Excel |
| POST | /api/import | 导入 Excel |

## 数据库设计

### users 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| username | VARCHAR(80) | 用户名 |
| email | VARCHAR(120) | 邮箱 |
| password_hash | VARCHAR(256) | 密码哈希 |
| created_at | DATETIME | 创建时间 |

### contacts 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| user_id | INT | 外键，关联用户 |
| name | VARCHAR(100) | 姓名 |
| is_favorite | BOOLEAN | 是否收藏 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### contact_methods 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| contact_id | INT | 外键，关联联系人 |
| type | VARCHAR(50) | 类型（phone/email/address/social） |
| value | VARCHAR(200) | 值 |

## 部署说明

1. 后端使用 Gunicorn + Nginx 部署
2. 前端执行 `npm run build`，将 dist 目录部署到 Nginx
3. 配置 Nginx 反向代理 API 请求

## 作者

软件工程课程 - 极限编程项目
