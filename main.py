from flask import Flask, jsonify
import asyncio
import aiohttp
import time
import schedule
from threading import Thread

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

def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def scheduled_task():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/status')
def status():
    results = run_async(make_requests())
    return jsonify(results)

def run_schedule():
    run_async(make_requests())  # Run immediately
    schedule.every(5).minutes.do(lambda: run_async(make_requests()))
    Thread(target=scheduled_task, daemon=True).start()

run_schedule()

if __name__ == "__main__":
    app.run(debug=True)