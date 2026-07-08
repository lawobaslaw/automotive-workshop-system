from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vehicles")
def vehicles():
    cars = [
        "Mercedes EQC",
        "BMW 320d",
        "Ford Focus",
        "Toyota Corolla"
    ]

    return render_template("vehicles.html", cars=cars)

if __name__ == "__main__":
    app.run(debug=True)