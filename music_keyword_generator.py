import openai

def generate_music_keyword(summary):
    prompt = f"이 뉴스 요약 리스트를 바탕으로 spotify 검색어 한문장으로 10자 이내로 창의적으로 만들어줘. 각 뉴스별로 따로 만들지말고 하나만 만들어줘. 그리고 이유도 설명해줘:\n{summary}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    lyrics = response.choices[0].message["content"]
    return lyrics