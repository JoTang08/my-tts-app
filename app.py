from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from edge_tts import voices, Communicate
from deep_translator import GoogleTranslator

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

async def generate_tts(text: str, voice: str, filename: str):
    communicate = Communicate(text, voice=voice)
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

    voices = await get_voices()
    available_voices = [v["ShortName"] for v in voices]

    if voice not in available_voices:
        raise HTTPException(status_code=400, detail=f"不支持的音色，支持：{available_voices}")
    if not text:
        raise HTTPException(status_code=400, detail="文本不能为空")

    filename = "static/output.mp3"
    await generate_tts(text, voice, filename)

    return FileResponse(filename, media_type="audio/mpeg")

def t(text):
    return GoogleTranslator(source="auto", target="zh-CN").translate(text)

@app.get("/voices")
async def get_voices():
    raw_voices = await voices.list_voices()
    result = []
    for v in raw_voices:
        result.append({
            "name": v["ShortName"],
            "gender": v["Gender"],
            "gender_zh": t(v["Gender"]),
            "locale": v["Locale"],
            "locale_zh": t(v["Locale"])
        })
    return result
