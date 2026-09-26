import requests
import os

SCHEDULING_SERVICE_URL = os.getenv(
    "SCHEDULING_SERVICE_URL",
    "http://127.0.0.1:5001"
)


def del_all_apointments(patient_id):
    response = requests.delete(
        f"{SCHEDULING_SERVICE_URL}/appointments/{patient_id}",
        timeout=3
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()