# 将语音列表的标签进行翻译，优化机制：设置翻译缓存
import json
from deep_translator import GoogleTranslator

# 载入缓存，避免重复翻译
try:
    with open("translate_cache.json", "r", encoding="utf-8") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

def translate_with_cache(text):
    if text in cache:
        return cache[text]
    try:
        translated = GoogleTranslator(source="en", target="zh-CN").translate(text)
        cache[text] = translated
        return translated
    except Exception:
        return text  # 出错返回原文

# 读取本地的 voices_data.json
with open("voices_data.json", "r", encoding="utf-8") as f:
    voices = json.load(f)

for voice in voices:
    personalities = voice.get("VoiceTag", {}).get("VoicePersonalities", [])
    translated = []
    for p in personalities:
        translated.append(translate_with_cache(p))
    voice.setdefault("VoiceTag", {})["VoicePersonalities_zh"] = translated

# 保存结果回 voices_data.json（如果想保留备份可另存）
with open("voices_data.json", "w", encoding="utf-8") as f:
    json.dump(voices, f, ensure_ascii=False, indent=2)

# 保存缓存文件
with open("translate_cache.json", "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
