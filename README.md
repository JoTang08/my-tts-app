### 🎙️ My TTS Project

> 一个使用 Python 实现的文本转语音（TTS）项目，基于微软 Edge TTS 引擎，提供语音列表接口和语音合成功能，支持中文语音合成，适用于内容创作、视频配音、语音助手等场景。

### ✨ 特性

- 使用 edge-tts 进行高质量语音合成
- 支持获取所有语音（voice）列表
- 提供 /tts API 接口合成 MP3 音频
- Web 前端界面调用测试
- 使用 uv 进行现代化 Python 依赖管理

### 🧰 环境准备

- Python >= 3.10
- 推荐使用 uv 替代 pipenv/poetry

```bash
# 安装 uv（一次性）
pip install uv

# 初始化项目环境
uv venv
source .venv/bin/activate
```

### 📦 安装依赖

```bash
uv pip install fastapi hypercorn edge-tts python-multipart deep-translator
```

### 🚀 启动服务

```
hypercorn app:app --reload
```

### 📑 接口说明

1. GET /voices
   获取支持的语音列表

返回字段包括：ShortName、Gender、Locale，可选翻译为中文

2. POST /tts

```bash
{
  "text": "你好，欢迎使用 TTS 服务！",
  "voice": "zh-CN-XiaoxiaoNeural"
}

```

- 成功时返回 .mp3 文件（audio/mpeg）

### 🌐 前端页面

将你自定义的 index.html 放入 static/ 目录。

访问 http://127.0.0.1:8000/ 即可打开测试界面。

### 📁 项目结构

```
my-tts-project/
├── app.py               # FastAPI 后端入口
├── static/              # 前端页面与生成音频存储目录
│   └── index.html
├── voices_cache.json    # 可选缓存语音列表
├── README.md            # 项目说明文档
├── pyproject.toml       # 依赖文件（uv 生成）

```
