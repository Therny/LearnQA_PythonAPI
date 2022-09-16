import requests
import time

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

response = requests.get(url)
parsed_responce = response.json()
token = parsed_responce["token"]
times = int(parsed_responce["seconds"])
print("Задача начата, время выполнения =" + str(parsed_responce["seconds"]))
playoad = {}
playoad["token"] = token
response_error = requests.get(url, params=playoad)
parsed_responce_error = response_error.json()
status = parsed_responce_error["status"]
if status == "Job is NOT ready":
    print("Джоба еще не готова")
else:
    print("Error!")
time.sleep(times)
response_success = requests.get(url, params=playoad)
parsed_responce_success = response_success.json()
status = parsed_responce_success["status"]
if status == "Job is ready":
    print("Задача выполнена")
    print("Результат: " + parsed_responce_success["result"])
else:
    print("Error2!")