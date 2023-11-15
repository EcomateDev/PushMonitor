import requests
import time
from flask import Flask
from threading import Thread
from webserver import keep_alive

app = Flask('')

@app.route('/')
def home():
    return "Monitor is active."

def run_web_server():
    def run():
        app.run(host='0.0.0.0', port=8080)

    t = Thread(target=run)
    t.start()

def check_site(url, interval_minutes):
    interval_seconds = interval_minutes * 60
    push_count = 1

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Site {url} is accessible.")
                # Simulating pushing by displaying information
                print(f"Push ID: {push_count}")
                print("Pushing successful!")
                print("[/] https://github.com/EcomateDev")
                print("[/] https://www.patreon.com/EcomateDev")
                # Incrementing push count
                push_count += 1
            else:
                print(f"Site {url} is inaccessible. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Connection error: {e}")

        time.sleep(interval_seconds)

def read_file_content(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

if __name__ == "__main__":
    url_file = "url.txt"
    time_file = "time.txt"

    run_web_server()

    while True:
        target_url = read_file_content(url_file)
        interval_minutes = int(read_file_content(time_file))

        if target_url:
            check_site(target_url, interval_minutes)
        else:
            print("No URL found in the file.")

        time.sleep(60)

keep_alive()
