import requests
import pytest

class TestAssertsCookie:
    def test_assert_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        assert "x-secret-homework-header" in response.headers, "There is no secret header in the response"

        header = response.headers.get('x-secret-homework-header')
        print('x-secret-homework-header: ', header)

        assert header == 'Some secret value', f"Value of secret-header is not 'Some secret value', new value = {header}"
