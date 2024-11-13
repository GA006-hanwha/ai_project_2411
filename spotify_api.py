import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os
import re

from flask import Flask, request

dotenv.load_dotenv()
# Spotify 개발자 대시보드에서 발급받은 값들
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_url='http://localhost:8888/callback'

scope = 'user-read-private user-read-playback-state user-modify-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth( 
    client_id=client_id, 
    client_secret=client_secret,
    redirect_uri=redirect_url,
    scope=scope
))

app = Flask(__name__)

@app.route('/play')
def play_music(keyword):
    keyword_parsed = re.findall(r'"(.*?)"', keyword)
    # 사용자가 '경쾌한 퇴근길' 검색어로 곡을 검색
    results = sp.search(q=keyword_parsed, limit=1)
    items = results['tracks']['items']
    
    if items:
        uri = items[0]['uri']
        track_id = uri.split(':')[2]
        print(track_id)

        # Spotify API에서 트랙 정보를 가져옴
        track_info = sp.track(track_id)
        preview_url = track_info['preview_url']

        if preview_url:
            print(preview_url)
            # HTML 코드로 Spotify 임베드 플레이어 제공
            return f'''<html><body>Spotify Player
                        <iframe src="https://open.spotify.com/embed/track/{track_id}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                        </body></html>'''
        else:
            return "미리듣기 URL이 없습니다."
    else:
        return "검색된 트랙이 없습니다."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)