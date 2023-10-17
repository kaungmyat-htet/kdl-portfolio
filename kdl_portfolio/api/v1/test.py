import requests
import json

url = 'http://local.overhang.io:8000/api/user/v1/accounts/kdl'
headers = {
    "Authorization": "Bearer 11g2GS8Xxe"
}

response = requests.get(url, headers=headers)

# You can also handle the response here, for example:
if response.status_code == 200:
    print("Request was successful!")
    # print(response.text)
    user_info = json.loads(response.text)
    user = {}
    if user_info["account_privacy"] != "all_user":
        user["name"] = user_info["name"]
        user["username"] = user_info["username"]
        user["email"] = user_info["email"]
        user["profile_image"] = user_info["profile_image"]
        user["bio"] = user_info["bio"]
        user["level_of_education"] = user_info["level_of_education"]
        user["social_links"] = user_info["social_links"]
        print(user)
    else:
        print("Sorry, the account is private.")
else:
    print(f"Request failed with status code {response.status_code}:")
    print(response.text)