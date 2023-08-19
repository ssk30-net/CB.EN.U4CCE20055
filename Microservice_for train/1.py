from flask import Flask, jsonify

app = Flask(_name_)

# Simulated train schedule data (replace with actual API calls)
train_data = [
    {
        "train_number": "123",
        "departure_time": "2023-08-19 12:00",
        "delay_minutes": 15,
        "sleeper_availability": 50,
        "ac_availability": 20,
        "sleeper_price": 100,
        "ac_price": 150,
    },
    # More train entries...
]


@app.route("/trains", methods=["GET"])
def get_train_schedules():
    current_time = datetime.now()

    relevant_trains = []
    for train in train_data:
        departure_datetime = datetime.strptime(train["departure_time"], "%Y-%m-%d %H:%M")
        adjusted_departure = departure_datetime + timedelta(minutes=train["delay_minutes"])

        if adjusted_departure > current_time + timedelta(minutes=30):
            relevant_trains.append(train)

    sorted_trains = sorted(
        relevant_trains,
        key=lambda x: (x["sleeper_price"], -x["sleeper_availability"], -x["delay_minutes"]),
    )

    return jsonify(sorted_trains)


if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000)