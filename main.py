from flask import Flask, jsonify
import asyncio
import aiohttp
import time
import schedule
import threading

app = Flask(__name__)

async def make_request(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return {
                "url": url,
                "status_code": response.status,
                "timestamp": time.ctime()
            }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "timestamp": time.ctime()
        }

async def make_requests():
    urls = [
        "https://nbbackend-vqt8.onrender.com",  # Replace with your first target website
        "https://model-microserve.onrender.com"   # Replace with your second target website
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    print(f"Requests made at {time.ctime()}")
    return results

def scheduled_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/status')
async def status():
    results = await make_requests()
    return jsonify(results)

def run_schedule():
    asyncio.run(make_requests())  # Run immediately
    schedule.every(5).minutes.do(lambda: asyncio.run(make_requests()))
    threading.Thread(target=scheduled_task, daemon=True).start()

if __name__ == "__main__":
    run_schedule()
    app.run(debug=True)