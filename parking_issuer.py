import requests
import json


UID = "12cdf204-d969-469a-9bd5-c1f1fc59ee34"


def refine_call1_to_call2(call1_response):
    refined_payload = {
        "email": call1_response.get("Email", ""),
        "PhoneNumber": call1_response.get("PhoneNumber", ""),
        "VehicleRegistrationCountry": call1_response.get("VehicleRegistrationCountry", ""),
        "Duration": call1_response.get("Duration", 0),
        "VehicleRegistration": call1_response.get("VehicleRegistration", ""),
        "parkingAreas": call1_response.get("ParkingAreas", []),
        "StartTime": call1_response.get("StartTime", ""),
        "EndTime": call1_response.get("EndTime", ""),
        "UId": call1_response.get("UId", ""),
        "Lang": call1_response.get("Lang", "da") or "da"
    }
    return refined_payload


def get_prepermit_response(license_plate, phone_no):
    url = "https://api.mobile-parking.eu/v10/permit/Tablet"

    payload = {
        "licensePlate": license_plate,
        "Uid": UID,
        "phoneNumber": phone_no,
        "email": "",    # Not provided in web version
        "delayedDate": "",
        "delayedDateTo": ""
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if not response.ok:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")

    parsed = response.json()

    call2_payload = refine_call1_to_call2(parsed)
    print(json.dumps(call2_payload, indent=2))

    return call2_payload


def run_parking_job(payload):
    url = "https://api.mobile-parking.eu/v10/permit/Tablet/confirm"

    payload["PhoneNumber"] = "45" + payload.get("PhoneNumber")
    payload["VehicleRegistration"] = payload["VehicleRegistration"]

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))


# if __name__ == "__main__":
#     payload = get_prepermit_response('bc12345', '12345678')
#     run_parking_job(payload)