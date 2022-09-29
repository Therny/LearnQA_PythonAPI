from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):
    remove_param = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):

        data = self.prepare_registration_data()
        data['email'] = 'vinkotovexample.com'
        response = MyRequests.post("/user/", data=data)
        print(response.text)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Check email = {data['email']}"

    @pytest.mark.parametrize('rm_param', remove_param)
    def test_create_user_without_some_parameters(self, rm_param):
        data = self.prepare_registration_data()
        data[rm_param] = None
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {rm_param}", \
            f"User is created, without param: {rm_param}"

    def test_create_user_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'v'
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Check username = {data['username']}"

    def test_create_user_long_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'vfdgjhjkfdhgkdslglsjhflgjhdflgjhsdkfjghldfjghsdljfhglsgjhlsdjfhglsjhgsldjdfgdfgsdgfsdfgsdfgsfgsdgsdfgsdfgsdfgsdfgsdfgfsdgsdfgsdgfgdsgdf\
        sfdgdfgsdfgdfgsdfgsdfgsdgdfgsfgsgdsgsdgsgfgsgsdgfsfgsfgdfgsfdgsfgsfgsfgsgfsfgsdgfgsg\
        sgsdfgsdfgsdgsdfgsdgfsdfgsdgsdgsgdsgfdgffdsgfhg'
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Check username = {data['username']}"