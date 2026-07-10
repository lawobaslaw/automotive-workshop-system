from flask import Flask, render_template
from database import Vehicle, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///workshop.db"

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vehicles")
def vehicles():
    cars = Vehicle.query.all()

    return render_template("vehicles.html", cars=cars)

@app.route("/jobs")
def jobs():

    jobs = [

        {
            "id":1001,
            "vehicle":"Mercedes EQC",
            "technician":"Larry",
            "status":"In Progress",
            "cost":450
        },

        {
            "id":1002,
            "vehicle":"BMW 320d",
            "technician":"John",
            "status":"Completed",
            "cost":220
        },

        {
            "id":1003,
            "vehicle":"Audi A6",
            "technician":"Mike",
            "status":"Waiting Parts",
            "cost":600
        }

    ]

    return render_template("jobs.html",jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)