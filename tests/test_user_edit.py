from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def setup(self):
        #Register
        register_data = self.prepare_registration_data()
        self.response1 = MyRequests.post("/user/", data=register_data)

        self.user_id = self.get_json_value(self.response1, 'id')
        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
    def test_edit_just_created_user(self):
        #check register
        Assertions.assert_code_status(self.response1, 200)
        Assertions.assert_json_has_key(self.response1, "id")

        #LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of user after edit"
        )

    def test_change_user_without_authorized(self):
        Assertions.assert_code_status(self.response1, 200)
        Assertions.assert_json_has_key(self.response1, "id")

        # EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == 'Auth token not supplied', f"Error, name was changed without authorize"

    def test_change_username_as_login_another_user(self):
        Assertions.assert_code_status(self.response1, 200)
        Assertions.assert_json_has_key(self.response1, "id")

        #LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Changed username"

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"username": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == 'Please, do not edit test users with ID 1, 2, 3, 4 or 5.', \
            f"Try edit userID = {self.user_id}"

        response4 = MyRequests.get(f"/user/{self.user_id}")

        Assertions.assert_json_value_by_name(
            response4,
            'username',
            'learnqa',
            f"Changed successfully?! New name='{new_name}', name after change='{response4.text}"
            )


    def test_edit_email_to_broken_email(self):
        #check register
        Assertions.assert_code_status(self.response1, 200)
        Assertions.assert_json_has_key(self.response1, "id")

        #LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_email = self.email.translate({ord('@'): None})

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == 'Invalid email format',\
            f"Email changed, old email='{self.email}', new email='{new_email}'"
        #GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            self.email,
            "Wrong email of user after edit")

    def test_edit_firstname_to_short(self):
        #check register
        Assertions.assert_code_status(self.response1, 200)
        Assertions.assert_json_has_key(self.response1, "id")

        #LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_firstname = 'V'

        response3 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstname}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, 'error', "Too short value for field firstName",
                                             "Changed firstName to very short")

        #GET
        response4 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            self.first_name,
            "Wrong firstName of user after edit")