from app import app

client = app.test_client()


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200


def test_vehicle_page():
    response = client.get("/vehicles")
    assert response.status_code == 200


def test_jobs_page():
    response = client.get("/jobs")
    assert response.status_code == 200


def test_add_vehicle_page():
    response = client.get("/vehicle/new")
    assert response.status_code == 200


def test_add_job_page():
    response = client.get("/jobs/new")
    assert response.status_code == 200