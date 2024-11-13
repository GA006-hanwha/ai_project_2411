import openai
import os
from dotenv import load_dotenv

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