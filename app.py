from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vehicles")
def vehicles():
    cars = [
        {
        "registration": "LP21 EQC",
        "make": "Mercedes",
        "model": "EQC",
        "year": 2021
    },
    {
        "registration": "BM19 320",
        "make": "BMW",
        "model": "320d",
        "year": 2019
    },
    {
        "registration": "FD20 FCS",
        "make": "Ford",
        "model": "Focus",
        "year": 2020
    },
    {
        "registration": "TY22 COR",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2022
    }
    ]

    return render_template("vehicles.html", cars=cars)

if __name__ == "__main__":
    app.run(debug=True)