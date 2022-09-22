import requests


url = "https://playground.learnqa.ru/api/homework_header"
response = requests.get(url)
header = response.headers.get('x-secret-homework-header')

print(header)
#d = {1: 2, 2: 4, 3: 9}
#print(d)
#print(d[1])