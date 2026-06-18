import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("CLICKUP_TOKEN")
team_id = os.getenv("TEAM_ID")

headers = {
    "Authorization": token
}

goal_name = f"Python Goal {int(time.time())}"
updated_goal_name = f"Updated Python Goal {int(time.time())}"

# CREATE GOAL
create_response = requests.post(
    f"https://api.clickup.com/api/v2/team/{team_id}/goal",
    headers=headers,
    json={
        "name": goal_name,
        "due_date": 1893456000000
    }
)

print("CREATE:", create_response.status_code)
assert create_response.status_code == 200

created_goal = create_response.json()["goal"]
goal_id = created_goal["id"]

assert created_goal["name"] == goal_name
assert goal_id is not None


# GET GOAL
get_response = requests.get(
    f"https://api.clickup.com/api/v2/goal/{goal_id}",
    headers=headers
)

print("GET:", get_response.status_code)
assert get_response.status_code == 200

get_goal = get_response.json()["goal"]
assert get_goal["id"] == goal_id
assert get_goal["name"] == goal_name


# UPDATE GOAL
update_response = requests.put(
    f"https://api.clickup.com/api/v2/goal/{goal_id}",
    headers=headers,
    json={
        "name": updated_goal_name
    }
)

print("UPDATE:", update_response.status_code)
assert update_response.status_code == 200

updated_goal = update_response.json()["goal"]
assert updated_goal["name"] == updated_goal_name


# DELETE GOAL
delete_response = requests.delete(
    f"https://api.clickup.com/api/v2/goal/{goal_id}",
    headers=headers
)

print("DELETE:", delete_response.status_code)
assert delete_response.status_code == 200


# NEGATIVE TEST WITHOUT TOKEN
negative_response = requests.get(
    f"https://api.clickup.com/api/v2/team/{team_id}/goal"
)

print("NEGATIVE:", negative_response.status_code)
assert negative_response.status_code in [400, 401]

print("All tests passed successfully!")