"# MCPP Image API

MCPP是一个基于FastAPI构建的图像处理API服务，提供多种图像分析和处理功能。

## 项目简介

MCPP Image API提供了一套完整的图像处理服务，包括主处理、大板块分析、小板块分析、地面分析和信息提取等功能。该服务采用RESTful API设计，支持多种图像输入格式和处理模式。

## 技术栈

- **FastAPI**: 高性能的Python Web框架
- **Pydantic V2**: 数据验证和设置管理
- **Requests**: HTTP客户端库
- **Uvicorn**: ASGI服务器
- **Docker**: 容器化部署支持

## 项目结构

```
code/
├── app/
│   ├── services/          # 图像处理服务模块
│   │   ├── MCPP_main.py   # 主处理服务
│   │   ├── MCPP_bigplate.py  # 大板块分析服务
│   │   ├── MCPP_smallplate.py  # 小板块分析服务
│   │   ├── MCPP_ground.py  # 地面分析服务
│   │   ├── MCPP_information.py  # 信息提取服务
│   │   ├── MCPP_batch.py  # 批量处理服务
│   │   ├── all_promot.py  # 提示词管理
│   │   └── __init__.py
│   ├── utils/             # 工具函数
│   │   ├── http.py        # HTTP请求工具
│   │   ├── logger.py      # 日志工具
│   │   ├── response.py    # 响应处理工具
│   │   └── __init__.py
│   ├── config.py          # 配置文件
│   ├── main.py            # API入口
│   ├── schemas.py         # 数据模型
│   └── __init__.py
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## 安装与运行

### 1. 环境准备

- Python 3.11+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建`.env`文件，配置必要的环境变量：

```env
API_KEY=your_api_key
API_URL=your_api_url
```

### 4. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

服务将在`http://localhost:8000`启动，API文档可在`http://localhost:8000/docs`访问。

### 5. Docker部署

```bash
docker build -t mcpp-image-api .
docker run -d -p 8000:8000 --env-file .env mcpp-image-api
```

## API文档

### 端点列表

| 端点 | 方法 | 描述 |
|------|------|------|
| `/run/main/upload` | POST | 主图像处理服务 |
| `/run/bigplate/upload` | POST | 大板块分析服务 |
| `/run/smallplate/upload` | POST | 小板块分析服务 |
| `/run/ground/upload` | POST | 地面分析服务 |
| `/run/information/upload` | POST | 信息提取服务 |
| `/run/batch/upload` | POST | 批量图像处理服务 |

### 请求格式

所有端点都接受`multipart/form-data`格式的请求，包含以下参数：

- `edit_image`: 需要处理的主图像文件
- `ref1`, `ref2`, `ref3`: 参考图像文件（可选）

### 响应格式

```json
{
  "status": "success",
  "output": "处理结果",
  "mode": "sync"  // 或 "async"
}
```

### 错误响应

```json
{
  "detail": "错误描述"
}
```

状态码：
- 400: 业务错误（模型问题、参数问题）
- 500: 系统错误

## 使用示例

### Python示例

```python
import requests

url = "http://localhost:8000/run/main/upload"
files = {
    "edit_image": open("image.jpg", "rb"),
    "ref1": open("ref1.jpg", "rb"),
    "ref2": open("ref2.jpg", "rb"),
    "ref3": open("ref3.jpg", "rb"),
}

response = requests.post(url, files=files)
print(response.json())
```

### cURL示例

```bash
curl -X POST "http://localhost:8000/run/main/upload" \
  -F "edit_image=@image.jpg" \
  -F "ref1=@ref1.jpg" \
  -F "ref2=@ref2.jpg" \
  -F "ref3=@ref3.jpg"
```

## 服务说明

### 主处理服务 (`/run/main/upload`)

提供完整的图像分析和处理功能，是最常用的服务端点。

### 大板块分析服务 (`/run/bigplate/upload`)

专门针对大板块图像进行分析和处理。

### 小板块分析服务 (`/run/smallplate/upload`)

针对小板块图像进行精细分析和处理。

### 地面分析服务 (`/run/ground/upload`)

专注于地面图像的分析和处理。

### 信息提取服务 (`/run/information/upload`)

从图像中提取关键信息。

### 批量处理服务 (`/run/batch/upload`)

支持批量处理多张图像。

## 配置说明

### 配置文件

`app/config.py`使用Pydantic Settings管理配置，支持从环境变量和`.env`文件加载配置。

### 主要配置项

- `API_KEY`: 访问上游服务的API密钥
- `API_URL`: 上游服务的API地址

## 日志和监控

服务使用结构化日志记录所有请求和处理过程，日志配置可在`app/utils/logger.py`中调整。

## 错误处理

服务实现了完善的错误处理机制：
- 业务错误（如参数错误、模型问题）返回400状态码
- 系统错误返回500状态码
- 所有错误都包含详细的错误描述

## 开发与贡献

### 开发环境设置

1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 创建`.env`文件并配置环境变量
4. 启动开发服务器：`uvicorn app.main:app --reload`

### 代码规范

- 遵循PEP 8代码风格
- 使用类型提示
- 编写清晰的文档字符串

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请联系项目维护人员。" 
