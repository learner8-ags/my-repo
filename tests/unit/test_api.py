from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def setup_function():
    client.post("/lab/reset")


def test_service_root_exposes_systems_collection():
    response = client.get("/redfish/v1")
    assert response.status_code == 200
    assert response.json()["Systems"]["@odata.id"] == "/redfish/v1/Systems"


def test_get_system_returns_redfish_style_resource():
    response = client.get("/redfish/v1/Systems/1")
    assert response.status_code == 200
    body = response.json()
    assert body["Id"] == "1"
    assert body["Manufacturer"] == "HPE"
    assert body["PowerState"] == "On"


def test_patch_asset_tag_is_supported():
    response = client.patch("/redfish/v1/Systems/1", json={"AssetTag": "RACK-B-42"})
    assert response.status_code == 200
    assert response.json()["AssetTag"] == "RACK-B-42"


def test_unknown_system_returns_404():
    response = client.get("/redfish/v1/Systems/99")
    assert response.status_code == 404
