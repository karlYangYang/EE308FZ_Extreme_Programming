# 通讯录后端 API

基于 Flask 框架开发的通讯录 RESTful API。

## 技术栈

- Flask 3.0
- MySQL + SQLAlchemy
- Flask-JWT-Extended (认证)
- openpyxl (Excel处理)

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

确保 MySQL 已安装并运行，创建数据库：

```sql
CREATE DATABASE addressbook CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置 MySQL 密码等信息。

### 4. 运行服务

```bash
python run.py
```

服务将在 http://localhost:5000 启动。

## API 文档

### 认证相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/logout` | POST | 用户登出 |
| `/api/auth/me` | GET | 获取当前用户信息 |

### 联系人管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/contacts` | GET | 获取联系人列表 |
| `/api/contacts` | POST | 创建联系人 |
| `/api/contacts/<id>` | GET | 获取联系人详情 |
| `/api/contacts/<id>` | PUT | 更新联系人 |
| `/api/contacts/<id>` | DELETE | 删除联系人 |
| `/api/contacts/<id>/favorite` | POST | 切换收藏状态 |
| `/api/contacts/<id>/methods` | POST | 添加联系方式 |
| `/api/contacts/<id>/methods/<mid>` | DELETE | 删除联系方式 |

### 导入导出

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/export` | GET | 导出 Excel |
| `/api/import` | POST | 导入 Excel |

## 请求示例

### 注册
```json
POST /api/auth/register
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456"
}
```

### 登录
```json
POST /api/auth/login
{
    "username": "testuser",
    "password": "123456"
}
```

### 创建联系人
```json
POST /api/contacts
Authorization: Bearer <token>
{
    "name": "张三",
    "is_favorite": true,
    "methods": [
        {"type": "phone", "value": "13800138000"},
        {"type": "email", "value": "zhangsan@example.com"}
    ]
}
```
