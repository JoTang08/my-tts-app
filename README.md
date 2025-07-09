##### 使用 uv 安装依赖

1. 创建 + 激活 + 退出 uv 环境
```
创建（仅需一次）：uv venv
激活：source .venv/bin/activate
退出：deactivate
```

2. 下载依赖
```
uv add edge-tts
```

3. 启动服务
```
uvicorn app:app --reload
```
