from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Missing YouTube video URL'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': False,
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            formats = []
            for f in info['formats']:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    label = f"{f['format_note']} ({f['ext']})"
                    formats.append({
                        'quality': label,
                        'resolution': f.get('height', 'audio'),
                        'url': f['url']
                    })
                elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'quality': 'audio (mp3)',
                        'url': f['url']
                    })

            return jsonify({
                'title': info['title'],
                'thumbnail': info['thumbnail'],
                'formats': formats
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
 import os

port = int(os.environ.get("PORT", 5000))  # Render sets this env variable
app.run(host='0.0.0.0', port=port)

