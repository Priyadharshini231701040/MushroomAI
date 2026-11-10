# MushroomAI

MushroomAI is a Flask website that runs a machine-learning model on an uploaded
mushroom image.

## Run locally

Use Python 3.11, then install the dependencies and start the app:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>.

## Deploy on Render

This repository includes a Render Blueprint in `render.yaml`. In Render, choose
**New + → Blueprint**, connect this repository, and create the service. Render
will install `requirements.txt` and start the Flask app with Gunicorn. The free
service may take a little time to wake up after inactivity.

## Safety

This is an educational demonstration, not a reliable mushroom identification
tool. Predictions may be wrong. Never eat a mushroom based on this website;
consult a qualified local expert.
