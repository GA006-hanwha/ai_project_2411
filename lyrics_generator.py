import openai

def generate_lyrics(summary):
    prompt = f"이 뉴스 요약을 바탕으로 락 발라드 스타일의 노래 가사를 한국어로 만들어줘:\n{summary}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    lyrics = response.choices[0].message["content"]
    return lyrics