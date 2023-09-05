import pytest
from api.controllers.controllers import app as test_app


@pytest.fixture()
def app():
    test_app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield test_app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


def test_process_image(client):
    image_url = "https://images.unsplash.com/photo-1581141849291-1125c7b692b5"

    response = client.post("/process_image", json={"image_url": image_url})
    data = response.get_json()

    assert response.status_code == 200
    assert "predictions" in data


def test_image_analysis(client):
    response = client.get("/image_analysis")
    data = response.get_json()

    assert response.status_code == 200
    assert "proper_ppe" in data
    assert "improper_ppe" in data
    assert "image_url" in data
    assert "image_location" in data
    assert "latitude" in data
    assert "longitude" in data
    assert "weather" in data
