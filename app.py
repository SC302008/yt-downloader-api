
from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing YouTube video URL'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'bestvideo+bestaudio/best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info['formats']:
                if f.get('url') and f.get('ext'):
                    formats.append({
                        'format_id': f.get('format_id'),
                        'extension': f.get('ext'),
                        'resolution': f.get('format_note') or f.get('height') or 'audio',
                        'url': f.get('url')
                    })

            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
