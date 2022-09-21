import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

metods = ["POST", "GET", "PUT", 'DELETE']
metods_not_in_list = ["HEAD", "PATCH"]

# Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае
print('1. http-запрос любого типа без параметра method')
for i in metods:
    response1 = requests.request(i, url)
    print(f"For {i} answer is "+"\""+response1.text+"\"")
print("-----------------------------")

# Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
print('2. http-запрос не из списка. Например, HEAD')
for k in metods_not_in_list:
    response2 = requests.request(k, url)
    print(f"For {k} answer is "+"\""+response2.text+"\"")

print("-----------------------------")

# Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
print('3. Делает запрос с правильным значением method.')
payload = {}
for i in metods:
    payload['method'] = i
    if i == "GET":
        response = requests.request(i, url, params=payload)
    else:
        response = requests.request(i, url, data=payload)
    print(f"For {i} answer is "+"\""+response.text+"\"")

print("-----------------------------")
# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
print('4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.')
payload = {}
for i in metods:
    for k in metods:
        payload['method'] = k
        if i == "GET":
            response = requests.request(i, url, params=payload)
        else:
            response = requests.request(i, url, data=payload)
        print(f"For {i}, method = {k} answer is "+"\""+response.text+"\"")