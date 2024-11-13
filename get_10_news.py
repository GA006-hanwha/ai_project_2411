import openai
import os
from dotenv import load_dotenv
from lyrics_generator import generate_lyrics
from music_generator import generate_music

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_news():
    prompt = "오늘의 글로벌 뉴스 10개를 각각 50자 이내로 간단하게 요약해줘. 각 뉴스는 번호를 매겨서 출력해줘."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response.choices[0].message["content"]
    return summary

if __name__ == "__main__":
    print("🔍 글로벌 뉴스 요약 중...")
    news_summary = summarize_news()
    print("✅ 뉴스 요약 완료:\n", news_summary)

    # print("🎵 가사 생성 중...")
    # lyrics = generate_lyrics(news_summary)
    # print("✅ 가사 생성 완료:\n", lyrics)

    # print("🎶 음악 생성 중...")
    # music_url = generate_music(lyrics)
    # print("✅ 음악 생성 완료! 음악 URL:\n", music_url)
