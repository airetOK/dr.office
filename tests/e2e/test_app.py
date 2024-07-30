from playwright.sync_api import expect, Playwright, Page


BASE_URL = 'http://localhost:5002'

def browser(test_func):
    def inner(playwright: Playwright):
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000)
        page = browser.new_page()
        test_func(page)
        browser.close()
    return inner


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
