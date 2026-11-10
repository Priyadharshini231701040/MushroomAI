from flask import Flask, render_template, request
from datetime import date
from pathlib import Path
from uuid import uuid4

import numpy as np
from PIL import Image
import joblib

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.context_processor
def inject_current_year():
    return {'current_year': date.today().year}

try:
    model = joblib.load(BASE_DIR / 'model.pkl')
    app.logger.info("Model loaded successfully")
except Exception:
    app.logger.exception("Unable to load model")
    model = None

@app.route('/')
def home():
    return render_template(
        'index.html',
        prediction=None,
        uploaded_image=None
    )

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template(
            'index.html',
            prediction="Model not loaded",
            result_class="poisonous",
            uploaded_image=None
        )

    file = request.files.get('file')
    if file is None:
        return render_template(
            'index.html',
            prediction="No file uploaded",
            result_class="poisonous",
            uploaded_image=None
        )

    if file.filename == '':
        return render_template(
            'index.html',
            prediction="No selected file",
            result_class="poisonous",
            uploaded_image=None
        )

    try:
        with Image.open(file.stream) as uploaded:
            image = uploaded.convert('RGB')
        image.thumbnail((1000, 1000))
        preview_path = app.config['UPLOAD_FOLDER'] / f'{uuid4().hex}.jpg'
        image.save(preview_path, format='JPEG')

        model_image = image.resize((64, 64))
        model_input = np.asarray(model_image).flatten().reshape(1, -1)
        prediction = model.predict(model_input)[0]

        if prediction == 0:
            result = "Edible 🍄"
            result_class = "edible"
        else:
            result = "Poisonous ☠️"
            result_class = "poisonous"
    except Exception:
        app.logger.exception("Unable to process uploaded image")
        result = "Unable to process this image. Please try another image."
        result_class = "poisonous"
        preview_path = None

    return render_template(
        'index.html',
        prediction=result,
        result_class=result_class,
        uploaded_image=preview_path.name if preview_path else None
    )

@app.errorhandler(413)
def request_entity_too_large(_error):
    return render_template(
        'index.html',
        prediction="Image is too large. Please upload an image under 10 MB.",
        result_class="poisonous",
        uploaded_image=None
    ), 413

if __name__ == '__main__':
    app.run(debug=False)
