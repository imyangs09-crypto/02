from playwright.sync_api import Page, expect

def test_python_search(page: Page):
    page.goto("https://www.python.org")
    page.fill("#id-search-field", "pytest")
    page.click("#submit")
    results = page.locator(".list-recent-events li")
    expect(results).to_have_count_greater_than(0)
    assert "pytest" in results.first.text_content().lower()

