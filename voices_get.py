# 获取微软语音列表，并保存本地
import asyncio
import json
from edge_tts import voices

async def save_voices():
    voice_list = await voices.list_voices()
    with open("voices_en.json", "w", encoding="utf-8") as f:
        json.dump(voice_list, f, ensure_ascii=False, indent=2)

asyncio.run(save_voices())