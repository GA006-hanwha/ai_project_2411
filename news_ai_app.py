import gradio as gr
import dotenv
from get_10_news import summarize_news
from music_keyword_generator import generate_music_keyword
from spotify_api import play_music

dotenv.load_dotenv()

# 뉴스 기사 요약 함수
def summarize():
    return summarize_news()

# 가사 변환 함수 (뉴스 기사 요약을 입력으로 받음)
def convert_to_music_keyword(news_summary):
    return generate_music_keyword(news_summary)

# Spotify 검색 및 재생 함수
def search_and_play_song(keyword):
    return play_music(keyword)

# Gradio 인터페이스 생성
with gr.Blocks(css=".gr-button { background-color: #3b5998; color: white; }") as iface:
    gr.Markdown(
        """
        # 📻 AI 기반 음악 추천 시스템
        이 애플리케이션은 최신 뉴스를 요약하고, 그 요약에서 음악 키워드를 생성한 후, Spotify에서 해당 음악을 재생합니다.
        
        1. **오늘의 뉴스**: 오늘의 뉴스를 요약합니다.
        2. **노래 검색 키워드 만들기**: 요약된 뉴스에서 음악 추천 키워드를 생성합니다.
        3. **키워드 노래 재생**: 생성된 키워드로 Spotify에서 음악을 검색하고 재생합니다.
        """,
        elem_id="title"
    )
    
    with gr.Row():
        news_button = gr.Button("📜 오늘의 뉴스", variant="primary")
        news_output = gr.Textbox(label="뉴스 기사 요약 결과", placeholder="오늘의 뉴스 요약이 여기에 표시됩니다.")
        news_button.click(fn=summarize, outputs=news_output)
    
    with gr.Row():
        keyword_button = gr.Button("🎼 노래 검색 키워드 만들기", variant="primary")
        keyword_output = gr.Textbox(label="키워드 결과", placeholder="생성된 키워드가 여기에 표시됩니다.")
        keyword_button.click(fn=convert_to_music_keyword, inputs=news_output, outputs=keyword_output)

    with gr.Row():
        play_button = gr.Button("🎶 키워드 노래 재생", variant="primary")
        play_output = gr.HTML("<p>Spotify에서 곡이 재생됩니다.</p>")
        play_button.click(fn=search_and_play_song, inputs=keyword_output, outputs=play_output)

iface.launch(server_name="0.0.0.0", server_port=8888, share=True)
