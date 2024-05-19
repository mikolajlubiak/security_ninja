import requests
import ast
import hashlib
import base64

url = "https://task.zostansecurity.ninja"

step_zero = requests.get(url)

first_step_code = step_zero.text.splitlines()[-1].split()[6]
first_step = requests.get(url + first_step_code)

second_step_challenge = first_step.text.splitlines()[-2].split()[2]
second_step_timestamp = first_step.text.splitlines()[-1].split()[2]
second_step = requests.get(url + "/?step=2", headers = {"X-challenge": second_step_challenge, "X-timestamp": second_step_timestamp})

third_step_challenge = second_step.text.splitlines()[4].split()[2]
third_step_timestamp = second_step.text.splitlines()[5].split()[2]
third_step_dict = second_step.text.splitlines()[10:10+22]
third_step_dict = ''.join(third_step_dict)
third_step_dict = ast.literal_eval(third_step_dict)
third_step_dict = dict(sorted(third_step_dict.items()))
third_step_dict_formatted = "&".join([f'{k}={v}' for k, v in third_step_dict.items()])
third_step_hash = hashlib.sha256(third_step_dict_formatted.encode()).hexdigest()
third_step = requests.post(url + "/?step=3", data={"challenge": third_step_challenge, "timestamp": third_step_timestamp, "hash": third_step_hash}, headers={'Content-Type': 'application/x-www-form-urlencoded'})

email = third_step.text.splitlines()[7]

while("@" not in email):
    encoded_bytes = email.encode("ascii")
    decoded_bytes = base64.b64decode(encoded_bytes)
    email = decoded_bytes.decode("ascii")

print(email)
