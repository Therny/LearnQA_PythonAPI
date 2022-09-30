from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

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

    def test_delete_user_id_2(self):

        login_data = {
            'email':  'vinkotov@example.com',
            'password': 1234
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            '/user/2',
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            "User with ID=2 deleted or changed"

        response3 = MyRequests.get(f"/user/2")

        Assertions.assert_json_value_by_name(
            response3,
            'username',
            'Vitaliy',
            f"User with ID=2 deleted or changed"
        )



    def test_delete_just_created_user(self):
        # check register
        Assertions.assert_code_status(self.response, 200)
        Assertions.assert_json_has_key(self.response, "id")

        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # CHECK
        response4 = MyRequests.get(f"/user/{self.user_id}")

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == 'User not found', f"Username '{self.username}', ID={self.user_id} not deleted"


    def test_delete_another_user(self):
        # check register setup user
        Assertions.assert_code_status(self.response, 200)
        Assertions.assert_json_has_key(self.response, "id")

        # LOGIN as userID=2
        login_data = {
            'email': 'vinkotov@example.com',
            'password': 1234
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        Assertions.assert_code_status(response1, 200)

        # DELETE setup user
        response2 = MyRequests.delete(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f" userID={self.user_id} was deleted or changed"

        # CHECK
        response3 = MyRequests.get(f"/user/{self.user_id}")

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            'username',
            self.username,
            f"Username '{self.username} with ID={self.user_id} deleted or changed"
        )
