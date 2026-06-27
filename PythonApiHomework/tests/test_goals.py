import os
import time

import pytest
import requests
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://api.clickup.com/api/v2"


def get_headers():
    token = os.getenv("CLICKUP_TOKEN")
    assert token is not None, "CLICKUP_TOKEN is missing"

    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }


def get_team_id():
    team_id = os.getenv("TEAM_ID")
    assert team_id is not None, "TEAM_ID is missing"
    return team_id


def create_goal():
    goal_name = f"Python Goal {int(time.time())}"

    response = requests.post(
        f"{BASE_URL}/team/{get_team_id()}/goal",
        headers=get_headers(),
        json={
            "name": goal_name,
            "due_date": 1893456000000
        }
    )

    assert response.status_code == 200

    goal = response.json()["goal"]

    assert goal["id"] is not None
    assert goal["name"] == goal_name

    return goal


def delete_goal(goal_id):
    response = requests.delete(
        f"{BASE_URL}/goal/{goal_id}",
        headers=get_headers()
    )

    assert response.status_code == 200


def test_full_goal_lifecycle():
    goal = create_goal()
    goal_id = goal["id"]

    try:
        get_response = requests.get(
            f"{BASE_URL}/goal/{goal_id}",
            headers=get_headers()
        )

        assert get_response.status_code == 200

        received_goal = get_response.json()["goal"]

        assert received_goal["id"] == goal_id
        assert received_goal["name"] == goal["name"]

        updated_goal_name = f"Updated Python Goal {int(time.time())}"

        update_response = requests.put(
            f"{BASE_URL}/goal/{goal_id}",
            headers=get_headers(),
            json={
                "name": updated_goal_name
            }
        )

        assert update_response.status_code == 200

        updated_goal = update_response.json()["goal"]

        assert updated_goal["name"] == updated_goal_name

    finally:
        delete_goal(goal_id)


def test_get_goals_without_token():
    goal = create_goal()
    goal_id = goal["id"]

    try:
        response = requests.get(
            f"{BASE_URL}/team/{get_team_id()}/goal"
        )

        assert response.status_code in [400, 401]

    finally:
        delete_goal(goal_id)