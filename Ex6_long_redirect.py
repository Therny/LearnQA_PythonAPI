import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)

print("Итоговый URL is " + "\"" + response.url + "\"")
count = len(response.history)
print("Кол-во редиректов = " + str(count))

