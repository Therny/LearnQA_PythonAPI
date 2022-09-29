# запуск тестов с allure
py -m pytest --alluredir=test_results/ tests/test_user_auth.py

# получение отчета allure
allure serve test_results

# запуск теста из класса
py -m pytest -s .\tests\test_user_edit.py -k test_edit_firstname_to_short

@pytest.mark.xfail()

@pytest.mark.parametrize()
