from flask import Flask, request, jsonify
from googletrans import Translator
from google.cloud import speech_v1p1beta1 as speech

app = Flask(__name__)

# Dịch ngôn ngữ sử dụng googletrans
translator = Translator()

# Route để nhận file âm thanh
@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files['file']
    text = speech_to_text(audio_file)
    
    if text:
        # Dịch văn bản sang tiếng Anh (nếu cần)
        detected_lang = translator.detect(text).lang
        if detected_lang != 'en':
            text = translator.translate(text, src=detected_lang, dest='en').text
        
        return jsonify({"text": text, "lang": detected_lang})
    else:
        return jsonify({"error": "Speech recognition failed"}), 500

# Hàm chuyển đổi giọng nói thành văn bản
def speech_to_text(audio_file):
    client = speech.SpeechClient()

    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="vi-VN",  # Bạn có thể thay đổi thành mã ngôn ngữ khác
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        return result.alternatives[0].transcript

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
