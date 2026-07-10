from flask import Flask, render_template, request, redirect, url_for
from database import Job, Vehicle, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///workshop.db"

db.init_app(app)

with app.app_context():
    db.create_all()



@app.route("/")
def home():
    total_vehicles = Vehicle.query.count()
    total_jobs = Job.query.count()
    completed_jobs = Job.query.filter_by(status="Completed").count()
    in_progress_jobs = Job.query.filter_by(status="In Progress").count()
    waiting_parts_jobs = Job.query.filter_by(status="Waiting Parts").count()
    return render_template("index.html", total_vehicles=total_vehicles, total_jobs=total_jobs, completed_jobs=completed_jobs, in_progress_jobs=in_progress_jobs, waiting_parts=waiting_parts_jobs)

@app.route("/vehicles")
def vehicles():
    cars = Vehicle.query.order_by(Vehicle.make).all()
    search=request.args.get("search")
    if search:
        cars = Vehicle.query.filter(Vehicle.registration.contains(search)).all()
    return render_template("vehicles.html", cars=cars)

@app.route("/jobs")
def jobs():

    jobs = Job.query.all()
    search=request.args.get("search")
    if search:
        jobs = Job.query.join(Vehicle).filter(Vehicle.registration.contains(search)).all()
    else:
        jobs = Job.query.all()
    return render_template("jobs.html", jobs=jobs)

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

    vehicle = Vehicle.query.get_or_404(id)

    db.session.delete(vehicle)

    db.session.commit()

    return redirect(url_for("vehicles"))

@app.route("/vehicle/edit/<int:id>", methods=["GET","POST"])
def edit_vehicle(id):

    vehicle = Vehicle.query.get_or_404(id)

    if request.method=="POST":

        vehicle.registration=request.form["registration"]

        vehicle.make=request.form["make"]

        vehicle.model=request.form["model"]

        vehicle.year=request.form["year"]

        db.session.commit()

        return redirect(url_for("vehicles"))

    return render_template(
        "add_vehicle.html",
        vehicle=vehicle
    )
@app.route("/jobs/new", methods=["GET", "POST"])
def add_job():

    vehicles = Vehicle.query.all()

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

    return render_template("add_job.html", vehicles=vehicles)
@app.route("/job/delete/<int:id>")
def delete_job(id):

    job = Job.query.get_or_404(id)

    db.session.delete(job)

    db.session.commit()

    return redirect(url_for("jobs"))

@app.route("/job/edit/<int:id>", methods=["GET", "POST"])
def edit_job(id):

    job = Job.query.get_or_404(id)
    vehicles = Vehicle.query.all()

    if request.method == "POST":

        job.vehicle_id = request.form["vehicle_id"]
        job.technician = request.form["technician"]
        job.status = request.form["status"]
        job.cost = float(request.form["cost"])

        db.session.commit()

        return redirect(url_for("jobs"))

    return render_template(
        "add_job.html",
        job=job,
        vehicles=vehicles
    )

if __name__ == "__main__":
    app.run(debug=True)