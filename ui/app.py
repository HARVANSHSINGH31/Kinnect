import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.db import get_db
import threading
import time

app = Flask(__name__)

# In-memory recognition log for the UI
recognition_log = []
detector_thread = None
detector_running = False

def log_recognition(name, confidence):
    recognition_log.insert(0, {
        "name": name,
        "confidence": confidence,
        "time": time.strftime("%H:%M:%S")
    })
    if len(recognition_log) > 50:
        recognition_log.pop()

@app.route("/")
def dashboard():
    db = get_db()
    people = db.execute("SELECT * FROM persons ORDER BY name").fetchall()
    db.close()
    return render_template("dashboard.html", people=people, log=recognition_log)

@app.route("/add_person", methods=["POST"])
def add_person():
    name = request.form.get("name", "").strip()
    relationship = request.form.get("relationship", "").strip()
    key_facts = request.form.get("key_facts", "").strip()

    if not name or not relationship:
        return redirect(url_for("dashboard"))

    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO persons (name, relationship, key_facts) VALUES (?, ?, ?)",
        (name, relationship, key_facts)
    )
    db.commit()
    db.close()

    os.makedirs(f"data/photos/{name}", exist_ok=True)
    return redirect(url_for("dashboard"))

@app.route("/delete_person/<int:person_id>", methods=["POST"])
def delete_person(person_id):
    db = get_db()
    db.execute("DELETE FROM persons WHERE id = ?", (person_id,))
    db.commit()
    db.close()
    return redirect(url_for("dashboard"))

@app.route("/api/log")
def api_log():
    return jsonify(recognition_log)

@app.route("/api/status")
def api_status():
    return jsonify({"running": detector_running})

@app.route("/api/start", methods=["POST"])
def api_start():
    global detector_thread, detector_running

    if detector_running:
        return jsonify({"status": "already running"})

    from recognition.detector import run_detector
    from voice.cue_generator import generate_cue
    from voice.player import speak

    def on_face_detected(name, confidence):
        log_recognition(name, confidence)
        db = get_db()
        person = db.execute(
            "SELECT * FROM persons WHERE name = ?", (name,)
        ).fetchone()
        db.close()

        if not person:
            return

        cue = generate_cue(person["name"], person["relationship"], person["key_facts"] or "")
        speak(cue)

    def run():
        global detector_running
        detector_running = True
        run_detector(on_face_detected, headless=True)
        detector_running = False

    detector_thread = threading.Thread(target=run, daemon=True)
    detector_thread.start()
    return jsonify({"status": "started"})

@app.route("/api/stop", methods=["POST"])
def api_stop():
    global detector_running
    detector_running = False
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)
