import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os

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
def play_music():
    results = sp.search(q='경쾌한 퇴근길', limit=1)
    items = results['tracks']['items']
    if items:
        uri = items[0]['uri']
        track_id = uri.split(':')[2]
        print(track_id)

    track_info = sp.track(track_id)
    print(track_info)
    preview_url = track_info['preview_url']

    if preview_url:
        print(preview_url)
    else:
        print("미리듣기 URL이 없습니다.")

    track_uri = request.args.get('track_uri')
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