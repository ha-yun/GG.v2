from flask import Flask, request, jsonify, send_file, render_template
import torch
import numpy as np
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wav
import os

app = Flask(__name__, template_folder="templates")

# MusicGen 모델 로드 (한 번 다운로드하면 캐시됨)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

@app.route("/song")
def index():
    return render_template("index.html")  # index.html을 웹에서 표시

@app.route("/generate", methods=["POST"])
def generate_music():
    try:
        data = request.get_json()
        user_prompt = data.get("style", "default music")

        # 사용자 입력을 텍스트 프롬프트로 변환
        inputs = processor(
            text=[user_prompt],
            padding=True,
            return_tensors="pt",
        )

        # 모델을 사용해 음악 생성
        with torch.no_grad():
            audio_values = model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=3,
                max_new_tokens=512
            )

        # 생성된 오디오 데이터를 NumPy 배열로 변환
        audio_array = audio_values.cpu().detach().numpy()
        sampling_rate = model.config.audio_encoder.sampling_rate

        # WAV 파일로 저장 (사용자 입력 기반으로 파일명 생성)
        filename = f"musicgen_{user_prompt.replace(' ', '_')}.wav"
        output_path = os.path.join("generated_music", filename)
        os.makedirs("generated_music", exist_ok=True)
        wav.write(output_path, rate=sampling_rate, data=audio_array[0, 0])

        return jsonify({"success": True, "filepath": f"/download/{filename}"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join("generated_music", filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)