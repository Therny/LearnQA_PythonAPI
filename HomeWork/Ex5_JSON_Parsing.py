import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
json_parse = json.loads(json_text)

for key, value in json_parse.items():
    print(value[1]['message'])


