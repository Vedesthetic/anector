from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_anomaly_score

app = Flask(__name__)
CORS(app)

FIELDS = [
    "keyIntervalMean", "keyIntervalStd", "mouseRate", "clickRate",
    "scrollRate", "tabSwitches", "answerChanges", "timeSpent"
]

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    features = [float(data[f]) for f in FIELDS]

    print("LIVE FEATURES:", features)

    score = get_anomaly_score(features)

    return jsonify({
        "risk_score": score,
        "status": risk_level(score)
    })

def risk_level(score):
    if score < 0.4:
        return "Normal"
    elif score < 0.7:
        return "Review"
    return "High Risk"

if __name__ == "__main__":
    app.run(debug=True)
