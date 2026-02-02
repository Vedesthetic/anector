# Anector

Anector is a privacy-preserving behavioral anomaly detection system for online assessments.

Instead of using webcams, screen recording, or intrusive surveillance, Anector analyzes
user interaction patterns (typing rhythm, mouse activity, focus changes) to flag unusual
exam behavior for human review.

## Why Anector?
- No webcam or screen capture
- No answer content analysis
- Privacy-first design
- Human-in-the-loop decision making

## How it works
1. Frontend tracks behavioral signals during an exam:
   - Typing speed & rhythm
   - Mouse activity
   - Tab switches
   - Time spent & edits
2. Backend processes these signals using:
   - Statistical feature extraction
   - Isolation Forest (unsupervised anomaly detection)
3. System returns a risk score:
   - Normal
   - Review
   - High Risk

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- ML: scikit-learn (Isolation Forest)

## Disclaimer
This system does NOT accuse students of cheating.
It flags unusual behavioral patterns for review while respecting user privacy.
