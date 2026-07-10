import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from database import Job, Vehicle, db

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Create tables if they do not exist
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # Optimised count queries executed in parallel/individually
    total_vehicles = db.session.query(Vehicle).count()
    total_jobs = db.session.query(Job).count()
    completed_jobs = db.session.query(Job).filter_by(status="Completed").count()
    in_progress_jobs = db.session.query(Job).filter_by(status="In Progress").count()
    waiting_parts_jobs = db.session.query(Job).filter_by(status="Waiting Parts").count()
    
    return render_template(
        "index.html", 
        total_vehicles=total_vehicles, 
        total_jobs=total_jobs, 
        completed_jobs=completed_jobs, 
        in_progress_jobs=in_progress_jobs, 
        waiting_parts=waiting_parts_jobs
    )


@app.route("/vehicles")
def vehicles():
    search = request.args.get("search", "").strip()
    
    # Bug fix: Filter the base query directly rather than executing twice
    if search:
        cars = db.session.query(Vehicle).filter(Vehicle.registration.contains(search)).all()
    else:
        cars = db.session.query(Vehicle).order_by(Vehicle.make).all()
        
    return render_template("vehicles.html", cars=cars)


@app.route("/jobs")
def jobs():
    search = request.args.get("search", "").strip()
    
    # Bug fix: Ensure the relationship join is handled correctly
    if search:
        jobs_list = db.session.query(Job).join(Vehicle).filter(Vehicle.registration.contains(search)).all()
    else:
        jobs_list = db.session.query(Job).all()
        
    return render_template("jobs.html", jobs=jobs_list)


@app.route("/vehicle/new", methods=["GET", "POST"])
def add_vehicle():
    if request.method == "POST":
        vehicle = Vehicle(
            registration=request.form["registration"],
            make=request.form["make"],
            model=request.form["model"],
            year=request.form["year"]
        )
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for("vehicles"))

    return render_template("add_vehicle.html")


@app.route("/vehicle/delete/<int:id>")
def delete_vehicle(id):
    vehicle = db.session.get(Vehicle, id) or Flask.abort(404)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for("vehicles"))


@app.route("/vehicle/edit/<int:id>", methods=["GET", "POST"])
def edit_vehicle(id):
    vehicle = db.session.get(Vehicle, id) or Flask.abort(404)

    if request.method == "POST":
        vehicle.registration = request.form["registration"]
        vehicle.make = request.form["make"]
        vehicle.model = request.form["model"]
        vehicle.year = request.form["year"]
        db.session.commit()
        return redirect(url_for("vehicles"))

    return render_template("add_vehicle.html", vehicle=vehicle)


@app.route("/jobs/new", methods=["GET", "POST"])
def add_job():
    vehicles_list = db.session.query(Vehicle).all()

    if request.method == "POST":
        job = Job(
            vehicle_id=request.form["vehicle_id"],
            technician=request.form["technician"],
            status=request.form["status"],
            cost=float(request.form["cost"])
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for("jobs"))

    return render_template("add_job.html", vehicles=vehicles_list)


@app.route("/job/delete/<int:id>")
def delete_job(id):
    job = db.session.get(Job, id) or Flask.abort(404)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for("jobs"))


@app.route("/job/edit/<int:id>", methods=["GET", "POST"])
def edit_job(id):
    job = db.session.get(Job, id) or Flask.abort(404)
    vehicles_list = db.session.query(Vehicle).all()

    if request.method == "POST":
        job.vehicle_id = request.form["vehicle_id"]
        job.technician = request.form["technician"]
        job.status = request.form["status"]
        job.cost = float(request.form["cost"])
        db.session.commit()
        return redirect(url_for("jobs"))

    return render_template("add_job.html", job=job, vehicles=vehicles_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
