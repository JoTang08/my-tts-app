import asyncio
import edge_tts
import time

async def main():
    ssml_text = "大家好，欢迎来到我的频道。今天，我们要聊一聊 Python 编程语言。Python 是一门非常强大且易学的语言，它适合初学者，也深受专业开发者喜爱。如果你刚开始学编程，不妨试试看 Python，相信你会喜欢它的简洁与高效。好啦，今天的分享就到这里，感谢收听！"

    start_time = time.perf_counter()
    communicate = edge_tts.Communicate(ssml_text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save("output.mp3")
    end_time = time.perf_counter()

    print(f"语音合成耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    asyncio.run(main())
