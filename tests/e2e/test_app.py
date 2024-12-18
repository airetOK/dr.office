from playwright.sync_api import expect, Playwright, Page
import pytest
import os
import sqlite3
from contextlib import closing
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
BASE_URL = os.getenv('E2E_HOST')
USERNAME = 'user'
PASSWORD = 'Qwerty1!'

def browser(test_func):
    def inner(playwright: Playwright):
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=100)
        page = browser.new_page()
        test_func(page)
        browser.close()
    return inner


@pytest.fixture(scope='module', autouse=True)
def before_tests():
    with closing(sqlite3.connect(os.getenv('DB_PATH'))) as conn:
        with conn:
            conn.execute(f"DELETE FROM patients WHERE user_id = (SELECT id FROM users WHERE username = '{USERNAME}')")
            conn.execute(f"DELETE FROM users WHERE username = '{USERNAME}'")
            

@browser
def test_check_tags_on_login_page(page: Page):
    page.goto(BASE_URL)
    assert page.locator('#login-username-input').is_visible()
    assert page.locator('#login-password-input').is_visible()
    expect(page.locator('#login-btn')).to_have_text('Увійти')

    page.locator('id=chevron-icon').click()
    page.locator('id=chevron-icon').click()
    assert page.locator('#register-username-input').is_visible()
    assert page.locator('#register-password-input').is_visible()
    expect(page.get_by_title('registration')).to_have_text('Реєстрація')

    page.locator('id=chevron-icon').click()
    assert not page.locator('#register-username-input').is_visible()
    assert not page.locator('#register-password-input').is_visible()

    page.locator('id=forget-chevron-icon').click()
    page.locator('id=forget-chevron-icon').click()
    assert page.locator('#forget-username-input').is_visible()
    assert page.locator('#forget-password-input').is_visible()
    expect(page.get_by_title('forget-password')).to_have_text('Забули пароль?')

    page.locator('id=forget-chevron-icon').click()
    assert not page.locator('#forget-username-input').is_visible()
    assert not page.locator('#forget-password-input').is_visible()


@browser
def test_register_user(page: Page):
    page.goto(BASE_URL)
    page.locator('id=chevron-icon').click()
    page.locator('id=chevron-icon').click()
    page.locator('#register-username-input').fill(USERNAME)
    page.locator('#register-password-input').fill(PASSWORD)
    page.locator('#register-btn').click()
    page.wait_for_url("**/")
    assert page.url == f"{BASE_URL}/"


@browser
def test_register_user_already_exists(page: Page):
    page.goto(BASE_URL)
    page.locator('id=chevron-icon').click()
    page.locator('id=chevron-icon').click()
    page.locator('#register-username-input').fill(USERNAME)
    page.locator('#register-password-input').fill(PASSWORD)
    page.locator('#register-btn').click()
    assert page.url == f"{BASE_URL}/register"
    expect(page.locator('id=error-message')).to_have_text('Користувач з таким ім\'ям існує')


@browser
def test_save_patient(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#addPatientLink').click()
    page.locator('#fullNameInput').fill('Test patient')
    page.locator('#selectActionOptionsLink').click()
    page.query_selector_all('.list-group-item')[6].click()
    page.locator('#saveActionOptionsButton').click()
    page.locator('#savePatient').click()
    assert 'Test patient' == page.query_selector_all('.fullNameHeader')[0].inner_text()
    assert '| Вторинне ендо (ліки) |' == page.query_selector_all('.patient-action')[0].inner_text()


@browser
def test_update_patient(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.query_selector_all('.updatePatientLink')[0].click()
    page.locator('#fullNameInput').fill('Test update patient')
    page.locator('#selectActionOptionsLink').click()
    page.query_selector_all('.list-group-item')[8].click()
    page.locator('#saveActionOptionsButton').click()
    page.locator('#savePatient').click()
    assert 'Test update patient' == page.query_selector_all('.fullNameHeader')[0].inner_text()
    assert '| Вторинне ендо (ліки) || Герметизація |' == page.query_selector_all('.patient-action')[0].inner_text()


@browser
def test_search_patient(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill('Test update')
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/fullName?searchValue=Test+update"
    elements = page.query_selector_all('.fullNameHeader')
    assert 'Test update patient' == elements[0].inner_text()
    assert '| Вторинне ендо (ліки) || Герметизація |' == page.query_selector_all('.patient-action')[0].inner_text()
    assert 1 == len(elements)


@browser
def test_search_patient_and_create_patient(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill('Test update')
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/fullName?searchValue=Test+update"

    page.locator('#addPatientLink').click()
    page.locator('#fullNameInput').fill('Test new patient')
    page.locator('#selectActionOptionsLink').click()
    page.query_selector_all('.list-group-item')[4].click()
    page.query_selector_all('.list-group-item')[5].click()
    page.query_selector_all('.list-group-item')[6].click()
    page.query_selector_all('.list-group-item')[7].click()
    page.locator('#saveActionOptionsButton').click()
    page.locator('#savePatient').click()
    assert 'Test new patient' == page.query_selector_all('.fullNameHeader')[0].inner_text()
    assert '| Вторинне ендо (ліки) || Герметизація |' == page.query_selector_all('.patient-action')[1].inner_text()
    assert 'Test update patient' == page.query_selector_all('.fullNameHeader')[1].inner_text()


@browser
def test_search_patient_and_update_patient(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill('Test new')
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/fullName?searchValue=Test+new"

    page.query_selector_all('.updatePatientLink')[0].click()
    page.locator('#fullNameInput').fill('Test update new patient')
    page.locator('#selectActionOptionsLink').click()
    page.query_selector_all('.list-group-item')[10].click()
    page.locator('#saveActionOptionsButton').click()
    page.locator('#savePatient').click()
    assert 'Test update new patient' == page.query_selector_all('.fullNameHeader')[0].inner_text()


@browser
def test_search_patient_by_action(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill('Герметизація')
    page.locator('#searchParam').select_option("actions")
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/actions?searchValue=%D0%93%D0%B5%D1%80%D0%BC%D0%B5%D1%82%D0%B8%D0%B7%D0%B0%D1%86%D1%96%D1%8F"
    assert 1 == len(page.query_selector_all('.fullNameHeader'))


@browser
def test_search_patient_by_date(page: Page):
    today_date = datetime.today().strftime('%d/%m/%Y')
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill(today_date)
    page.locator('#searchParam').select_option("date")
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/date?searchValue={'%2F'.join(today_date.split('/'))}"
    assert 2 == len(page.query_selector_all('.fullNameHeader'))


@browser
def test_search_patient_by_empty_fullName(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill("")
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/fullName?searchValue="
    assert 2 == len(page.query_selector_all('.fullNameHeader'))
    

@browser
def test_search_patient_by_empty_actions(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill("")
    page.locator('#searchParam').select_option("actions")
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/actions?searchValue="
    assert 2 == len(page.query_selector_all('.fullNameHeader'))


@browser
def test_search_patient_by_not_exist_fullName(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill("Non exist")
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/fullName?searchValue=Non+exist"
    assert 0 == len(page.query_selector_all('.fullNameHeader'))
    expect(page.locator('#no-patients-msg')).to_have_text('Пацієнтів немає.')


@browser
def test_search_patient_by_not_exist_actions(page: Page):
    page.goto(BASE_URL)
    page.locator('#login-username-input').fill(USERNAME)
    page.locator('#login-password-input').fill(PASSWORD)
    page.locator('#login-btn').click()
    page.locator('#searchInput').fill("Non exist")
    page.locator('#searchParam').select_option("actions")
    page.locator('#searchButton').click()
    assert page.url == f"{BASE_URL}/search/actions?searchValue=Non+exist"
    assert 0 == len(page.query_selector_all('.fullNameHeader'))
    expect(page.locator('#no-patients-msg')).to_have_text('Пацієнтів немає.')