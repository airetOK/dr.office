import re
from playwright.sync_api import sync_playwright, expect, Playwright, Browser, Page


BASE_URL = 'http://localhost:5002'


def open_close_browsers(func):
    def inner(playwright: Playwright):
        chrome_browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000)
        func(chrome_browser)
        chrome_browser.close()
    return inner


@open_close_browsers
def test_redirect_to_login_page(chrome_browser: Browser):
    expect(__login_page(chrome_browser)).to_have_url(
        re.compile(f'{BASE_URL}/login'))


@open_close_browsers
def test_add_patient(chrome_browser: Browser):
    page = __login_page(chrome_browser)
    page = __login(page)
    page.locator('.fa-plus-circle').click()
    page.locator('#fullNameInput').fill('TestUser')
    page.locator('#savePatient').click(force=True)


@open_close_browsers
def test_add_patients_and_move_to_page_2(chrome_browser: Browser):
    page = __login_page(chrome_browser)
    page = __login(page)
    for i in range(11):
        page.locator('.fa-plus-circle').click()
        page.locator('#fullNameInput').fill('TestUser')
        page.locator('#savePatient').click(force=True)

    page.locator('.fa-arrow-right').click()


def __login_page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f'{BASE_URL}')
    return page


def __login(page: Page):
    page.locator('#Username').fill('user')
    page.locator('#password').fill('test')
    page.get_by_role('button').click()
    return page
