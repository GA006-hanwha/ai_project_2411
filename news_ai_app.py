import gradio as gr

# 함수 정의: 입력된 텍스트를 받아 특정 결과를 반환하는 함수
def text_processing(input_text):
    # 특정 결과 예시: 입력된 텍스트에 대한 간단한 응답 생성
    return f"입력하신 텍스트는: {input_text}"

# Gradio 인터페이스 생성
# inputs는 텍스트박스, outputs는 텍스트로 설정
iface = gr.Interface(fn=text_processing, 
                     inputs="text", 
                     outputs="text", 
                     title="뉴스 음악 만들기",
                     description="최근 뉴스 검색 결과를 바탕으로 음악을 생성해 줍니다.")

# Gradio 인터페이스 실행
iface.launch()