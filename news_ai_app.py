import gradio as gr
from get_10_news import summarize_news
from lyrics_generator import generate_lyrics
from music_generator import generate_music

# 뉴스 기사 요약 함수
def summarize():
    return summarize_news()

# 가사 변환 함수 (뉴스 기사 요약을 입력으로 받음)
def convert_to_lyrics(news_summary):
    return generate_lyrics(news_summary)

# Gradio Blocks 인터페이스 생성
with gr.Blocks() as iface:
    # 뉴스 기사 요약하기 버튼과 출력
    with gr.Row():
        news_button = gr.Button("오늘의 뉴스")
        news_output = gr.Textbox(label="뉴스 기사 요약 결과")
        news_button.click(fn=summarize, outputs=news_output)
    
    # 가사로 변환하기 버튼과 출력
    with gr.Row():
        lyrics_button = gr.Button("🎶")
        lyrics_output = gr.Textbox(label="가사 변환 결과")
        # 가사 변환 버튼 클릭 시 뉴스 요약을 인풋으로 전달
        lyrics_button.click(fn=convert_to_lyrics, inputs=news_output, outputs=lyrics_output)

# Gradio 인터페이스 실행
iface.launch(autoreload=True)
