from copy import deepcopy
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="HPE Redfish-Style Lab Service",
    version="0.1.0",
    description="Small Redfish-inspired API used for the Agentic SDLC training lab.",
)

SYSTEM_TEMPLATE = {
    "@odata.id": "/redfish/v1/Systems/1",
    "@odata.type": "#ComputerSystem.v1_20_0.ComputerSystem",
    "Id": "1",
    "Name": "HPE Lab Server",
    "Manufacturer": "HPE",
    "Model": "ProLiant-Agentic-Lab",
    "SerialNumber": "LAB-SN-0001",
    "AssetTag": "TRAINING-RACK-A",
    "PowerState": "On",
    "Oem": {"Hpe": {"LastResetType": None}},
}

system_state = deepcopy(SYSTEM_TEMPLATE)


class SystemPatch(BaseModel):
    # Intentionally minimal for the starter lab. The bug ticket exposes
    # an input-validation issue that the learner's agent must diagnose.
    AssetTag: Optional[str] = None


def system_or_404(system_id: str) -> dict:
    if system_id != "1":
        raise HTTPException(status_code=404, detail="System not found")
    return system_state


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/redfish/v1")
def service_root() -> dict:
    return {
        "@odata.id": "/redfish/v1",
        "@odata.type": "#ServiceRoot.v1_15_0.ServiceRoot",
        "Id": "RootService",
        "Name": "HPE Agentic Lab Redfish Service",
        "Systems": {"@odata.id": "/redfish/v1/Systems"},
    }


@app.get("/redfish/v1/Systems")
def systems_collection() -> dict:
    return {
        "@odata.id": "/redfish/v1/Systems",
        "@odata.type": "#ComputerSystemCollection.ComputerSystemCollection",
        "Name": "Computer System Collection",
        "Members@odata.count": 1,
        "Members": [{"@odata.id": "/redfish/v1/Systems/1"}],
    }


@app.get("/redfish/v1/Systems/{system_id}")
def get_system(system_id: str) -> dict:
    return system_or_404(system_id)


@app.patch("/redfish/v1/Systems/{system_id}")
def patch_system(system_id: str, patch: SystemPatch) -> dict:
    system = system_or_404(system_id)
    if patch.AssetTag is not None:
        system["AssetTag"] = patch.AssetTag
    return system


@app.post("/lab/reset")
def reset_lab_state() -> dict:
    """Training-only endpoint so tests/demos can restore deterministic state."""
    system_state.clear()
    system_state.update(deepcopy(SYSTEM_TEMPLATE))
    return {"status": "reset"}
