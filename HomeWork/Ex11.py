import requests
import pytest

class TestAssertsCookie:
    def test_assert_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        assert 'HomeWork' in response.cookies, "Not find cookie in response"
        cookies = dict(response.cookies)
        print(cookies)

        assert cookies == {'HomeWork': 'hw_value'}, f"Cookie '{cookies}' is not assert with print(cookie): 'HomeWork': 'hw_value'"