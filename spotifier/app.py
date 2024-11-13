import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os

from flask import Flask, request, redirect, session

dotenv.load_dotenv()
# Spotify 개발자 대시보드에서 발급받은 값들
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_url='http://localhost:8888/callback'

scope = 'user-read-private user-read-playback-state user-modify-playback-state'
scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth( 
    client_id=client_id, 
    client_secret=client_secret,
    redirect_uri=redirect_url,
    scope=scope
))

app = Flask(__name__)

@app.route('/callback/')
def callback():
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_url,
                            scope=scope)
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    # 토큰 정보 저장 (session 또는 데이터베이스)
    session['token_info'] = token_info

    # 사용자 정보 가져오기 (예시)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    print(user['display_name'])

    return redirect('/play')  # 인증 후 이동할 페이지

@app.route('/login')
def login():
  sp_oauth = SpotifyOAuth(client_id=client_id, 
                          client_secret=client_secret, 
                          redirect_uri=redirect_url, 
                          scope=scope)
  auth_url = sp_oauth.get_authorize_url()

  return redirect(auth_url)

@app.route('/play')
def play_music():
    items = request.args.get('items', "Spring,Summer,Autumn,Winter")
    tracks = []

    for idx, i in enumerate(items.split(',')):
        i=i.strip()
        print(f"[{idx}] {i}")
        results = sp.search(q=i, limit=1)
        items = results['tracks']['items']
        if items:
            uri = items[0]['uri']
            track_id = uri.split(':')[2]
            tracks.append(track_id)
            print(f'track_id : {track_id}')
        else:
            print(f'skip for {i}')

    # results = sp.search(q='우울한 출근길', limit=1)
    # items = results['tracks']['items']
    # if items:
    #     uri = items[0]['uri']
    #     track_id = uri.split(':')[2]
    #     tracks.append(track_id)
    #     print(track_id)
    


    track_info = sp.track(track_id)
    print(f'track_info:{track_info}')
    print(f'tracks={len(tracks)}')
    # preview_url = track_info['preview_url']

    user = sp.current_user()
    user_id = user['id']
    playlist = sp.user_playlist_create(user=user_id, name='newsmusic', public=True)
    playlist_id = playlist['id']
    results = sp.playlist_add_items(playlist_id, tracks)
    print('created playlist:', playlist_id)
    print(results)

    # if preview_url:
    #     print(preview_url)
    # else:
    #     print("미리듣기 URL이 없습니다.")

    track_uri = request.args.get('track_uri')
    iframe=f'<iframe src="https://open.spotify.com/embed/playlist/{playlist_id}" width="300" height="640" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
    print(f'iframe:{iframe}')
    return f'<html><body>Hello{iframe}</body></html>'
    return f'<html><body>Hello<iframe src="https://open.spotify.com/embed/track/{track_id}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe></body></html>'
    # sp.start_playback(uris=[preview_url])
    return '''<html><head>
    <script src="https://open.spotify.com/embed/iframe-api/v1" async></script>
    </head><body>Hello
    <div id="embed-iframe"></div> <button id="play">Play Music</button>
    <script>
    window.onSpotifyIframeApiReady = (IFrameAPI) => {
        const element = document.getElementById('embed-iframe');
        const options = {
            uri: 'spotify:track:YOUR_TRACK_ID'
        };
        const callback = (EmbedController) => {
            document.getElementById('play').onclick = () => {
                EmbedController.play();
            }, 1000);
        };
        IFrameAPI.createController(element, options, callback);
        };
    </script>
    </body></html>'''.replace("YOUR_TRACK_ID", track_id)
    return '<html><body>https://p.scdn.co/mp3-preview/243c0d6c751c96b538ad459aba84764ed9fe8e49?cid=afa8a16d2548496ebc6518732ffda1a3</body>'
    #return 'Music started playing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)