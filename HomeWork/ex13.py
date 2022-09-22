import requests
import pytest

class TestUserAgent:
    user_agents = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', '"platform": "Mobile", "browser": "No", "device": "Android"'),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            '"platform": "Mobile", "browser": "Chrome", "device": "iOS"'),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            '"platform": "Googlebot", "browser": "Unknown", "device": "Unknown"'),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            '"platform": "Web", "browser": "Chrome", "device": "No"'),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            '"platform": "Mobile", "browser": "No", "device": "iPhone"')
    ]
    @pytest.mark.parametrize('user_agent, expected', user_agents)
    def test_agent_check(self, user_agent, expected):
        url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'

        response = requests.get(url, headers={"User-Agent": user_agent})

        assert response.status_code == 200, "Wrong response code"

        parsed_response = response.json()

        assert 'platform' in parsed_response['platform'], "Answer haven't 'Platform'"

        assert parsed_response["platform"] == expected["platform"], f"Response platform '{parsed_response['platform']}' not value '{expected['platform']}', for agents: {user_agent}"
#            assert parsed_response["browser"] == value["browser"], f"Response browser '{parsed_response['browser']}' not value '{value['browser']}', for agents: {key}"
#            assert parsed_response["device"] == value["device"], f"Response device '{parsed_response['device']}' not value '{value['device']}', for agents: {key}"


