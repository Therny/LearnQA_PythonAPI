from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic("User delete cases")
class TestUserDelete(BaseCase):
    def setup(self):
        # Register
        register_data = self.prepare_registration_data()
        self.response = MyRequests.post("/user/", data=register_data)

        self.user_id = self.get_json_value(self.response, 'id')
        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.username = register_data['username']

    @allure.title('Try delete userID=2, it cannot be deleted')
    @allure.description("This test check that userId= cannot deleted")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_delete_user_id_2(self):

        login_data = {
            'email':  'vinkotov@example.com',
            'password': 1234
        }
        with allure.step('Login as Id=2'):
            response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        with allure.step('Try delete userId=2'):
            response2 = MyRequests.delete(
                '/user/2',
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            "User with ID=2 deleted or changed"

        with allure.step('Get data for UserId=2'):
            response3 = MyRequests.get(f"/user/2")

        Assertions.assert_json_value_by_name(
            response3,
            'username',
            'Vitaliy',
            f"User with ID=2 deleted or changed"
        )


    @allure.title('Create new user and delete him')
    @allure.description("This test check delete user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_just_created_user(self):
        # check register
        Assertions.assert_code_status(self.response, 200)
        Assertions.assert_json_has_key(self.response, "id")

        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }
        with allure.step('Get data for New User'):
            response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        with allure.step('Delete user'):
            response3 = MyRequests.delete(
                f"/user/{self.user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # CHECK
        with allure.step('Check that user was deleted'):
            response4 = MyRequests.get(f"/user/{self.user_id}")

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == 'User not found', f"Username '{self.username}', ID={self.user_id} not deleted"

    @allure.title('Create new user and delete him, as logged another user')
    @allure.description("This test check delete user then logged another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_another_user(self):
        # check register setup user
        Assertions.assert_code_status(self.response, 200)
        Assertions.assert_json_has_key(self.response, "id")

        # LOGIN as userID=2
        login_data = {
            'email': 'vinkotov@example.com',
            'password': 1234
        }
        with allure.step('login as UserId=2'):
            response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        Assertions.assert_code_status(response1, 200)

        # DELETE setup user
        with allure.step('try deleted new user'):
            response2 = MyRequests.delete(
                f"/user/{self.user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f" userID={self.user_id} was deleted or changed"

        # CHECK
        with allure.step('Check that user not deleted'):
            response3 = MyRequests.get(f"/user/{self.user_id}")

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            'username',
            self.username,
            f"Username '{self.username} with ID={self.user_id} deleted or changed"
        )
