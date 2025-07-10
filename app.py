from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from edge_tts import Communicate
import asyncio
import json

# 全局加载一次（推荐）
with open("voices_data.json", "r", encoding="utf-8") as f:
    voices_data = json.load(f)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

async def generate_tts(text: str, voice: str, filename: str, rate: str = "+0%"):
    communicate = Communicate(text, voice=voice, rate=rate)
    await communicate.save(filename)

@app.get("/", response_class=HTMLResponse)
async def homepage():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data.get("text", "")
    voice = data.get("voice", "zh-CN-XiaoxiaoNeural")
    rate = data.get("rate", "+0%")  # ← 增加默认 rate 参数,控制语速

    voices = voices_data
    available_voices = [v["ShortName"] for v in voices]

    if voice not in available_voices:
        raise HTTPException(status_code=400, detail=f"不支持的音色，支持：{available_voices}")
    if not text:
        raise HTTPException(status_code=400, detail="文本不能为空")

    filename = "static/output.mp3"
    await generate_tts(text, voice, filename, rate=rate)  # ← 把 rate 传进去

    return FileResponse(filename, media_type="audio/mpeg")

@app.get("/voices")
async def get_voices():
    try:
        # 给网络请求设置超时，比如10秒
        raw_voices = voices_data
        list = []
        for v in raw_voices:
            voice_personalities_zh = v.get("VoiceTag", {}).get("VoicePersonalities_zh", [])
            list.append({
                "名称": v["ShortName"],
                "性别": "男性" if v["Gender"] == "Male" else "女性",
                "语言": v["Locale_zh"],
                "风格": voice_personalities_zh
            })
        return list

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="获取语音列表超时，请稍后重试")
    except Exception as e:
        # 打印异常日志方便调试（可以用 logging 替代 print）
        print(f"获取语音列表异常: {e}")
        raise HTTPException(status_code=500, detail="服务器内部错误")
