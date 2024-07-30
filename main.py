from flask import Flask, jsonify
import requests
import time
import schedule
import threading

app = Flask(__name__)

def make_requests():
    urls = [
        "https://nbbackend-vqt8.onrender.com",  # Replace with your first target website
        "https://model-microserve.onrender.com/"   # Replace with your second target website
    ]
    results = []
    for url in urls:
        try:
            response = requests.get(url)
            results.append({
                "url": url,
                "status_code": response.status_code,
                "timestamp": time.ctime()
            })
        except requests.RequestException as e:
            results.append({
                "url": url,
                "error": str(e),
                "timestamp": time.ctime()
            })
    return results

def scheduled_task():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/status')
def status():
    return jsonify(make_requests())

def run_schedule():
    make_requests()  # Run immediately
    schedule.every(5).minutes.do(make_requests)
    threading.Thread(target=scheduled_task, daemon=True).start()

if __name__ == "__main__":
    run_schedule()
    app.run(debug=True)