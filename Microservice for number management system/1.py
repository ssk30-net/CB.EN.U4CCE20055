from flask import Flask, request, jsonify
import requests
import time
import concurrent.futures

app = Flask(_name_)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            if "numbers" in data and isinstance(data["numbers"], list):
                return data["numbers"]
    except requests.exceptions.Timeout:
        pass  # Ignore timeouts
    except:
        pass  # Ignore other errors
    return []

@app.route("/numbers", methods=["GET"])
def get_merged_numbers():
    urls = request.args.getlist("url")
    unique_numbers = set()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            numbers = future.result()
            unique_numbers.update(numbers)

    response_data = {"numbers": sorted(unique_numbers)}
    return jsonify(response_data)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=3000)