from playwright.sync_api import expect, Playwright, Page
import pytest
import sqlite3
from contextlib import closing


BASE_URL = 'http://localhost:5002'
USERNAME = 'user'
PASSWORD = 'Qwerty1!'

def browser(test_func):
    def inner(playwright: Playwright):
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000)
        page = browser.new_page()
        test_func(page)
        browser.close()
    return inner


@pytest.fixture(scope='module', autouse=True)
def before_tests():
    with closing(sqlite3.connect('patients.db')) as conn:
        with conn:
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
