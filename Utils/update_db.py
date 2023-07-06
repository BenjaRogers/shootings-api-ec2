import json
import requests
from dotenv import load_dotenv, dotenv_values
import pandas as pd

load_dotenv()
env_vars = dotenv_values()
username = env_vars["username"]
password = env_vars["password"]

base_url = "http://localhost:5000/"


def get_token():
    response = requests.get(base_url + "login", auth=(username, password))
    return json.loads(response.content)["token"]


def get_old_data():
    response = requests.get(base_url + "person", headers=headers)
    return json.loads(response.content)


def get_new_data():
    github_url = (
        url
    ) = r"https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/v1/fatal-police-shootings-data.csv"
    new_data_df = pd.read_csv(github_url)
    new_data = json.loads(new_data_df.to_json(orient="records", index=True))
    return new_data


def update_record(new_person, old_person):
    for key in new_person:
        if str(new_person[key]) != str(old_person[key]):
            response = requests.put(
                base_url + f"person/{new_person['id']}",
                data=json.dumps(new_person),
                headers=headers,
            )
            print(f"update record {new_person['id']}")
            return response.status_code


headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "x-access-token": get_token(),
}


def update_database():
    old_data = get_old_data()
    new_data = get_new_data()
    # Compare each record in new data to old records
    #     if id is the same and data is different -> update

    for new_person in new_data:
        in_old_data = False
        for old_person in old_data["people"]:
            if new_person["id"] == int(old_person["id"]):
                in_old_data = True
                print(str(new_person["id"]) + " is in old data")
                update_record(new_person, old_person)

        # if id is new -> add to db
        if in_old_data == False:
            print(str(new_person["id"]) + " is not in old data... adding to db")
            response = requests.post(
                base_url + "/person", data=json.dumps(new_person), headers=headers
            )
            print(response.status_code)

    # if id is not in new data but in old data -> delete
    for old_person in old_data["people"]:
        in_new_data = False
        for new_person in new_data:
            if str(old_person["id"]) == str(new_person["id"]):
                in_new_data = True
                break
        if not in_new_data:
            response = requests.delete(
                base_url + "person/" + str(old_person["id"]), headers=headers
            )
            print(response.status_code)


def batch_add():
    new_data = get_new_data()
    for person in new_data:
        response = requests.post(
            base_url + "person", data=json.dumps(person), headers=headers
        )
        print(response.status_code)


update_database()
