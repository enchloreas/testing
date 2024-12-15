from playwright.sync_api import sync_playwright
import os
import requests
import pytest

# Ensure the traces directory exists
def ensure_traces_directory():
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces")
    os.makedirs(traces_path, exist_ok=True)
    return traces_path

# def ensure_traces_directory():
#     #Ensure the traces directory exists.
#    if not os.path.exists("traces"):
#         os.makedirs("traces")


def verify_broken_links(page):
    """Check all links on the page for HTTP errors."""
    links = page.locator("a").all()
    for link in links:
        href = link.get_attribute("href")
        if href:
            response = requests.get(href)
            assert response.status_code == 200, f"Broken link: {href}"

def test_website_loads():
    ensure_traces_directory()
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=traces_path)
        page = context.new_page()
        response = page.goto("https://www.saucedemo.com/")

        # Verify HTTP response status
        assert response.status == 200, "Failed to load the website"

        # Verify page title
        assert "Swag Labs" in page.title(), "Title is missing or incorrect"

        # Verify logo visibility
        assert page.locator("div.login_logo").is_visible(), "Logo is missing"

        context.close()
        browser.close()

def test_navigation_links():
    ensure_traces_directory()
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=traces_path)
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")

        # Verify navigation links (login buttons and other links)
        links = ["#login-button"]  # Example for the test website
        for link in links:
            assert page.locator(link).is_visible(), f"Link {link} is not visible"

        context.close()
        browser.close()

def test_login_functionality():
    ensure_traces_directory()
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=traces_path)
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")

        # Login attempt
        page.fill("input#user-name", "standard_user")
        page.fill("input#password", "secret_sauce")
        page.click("input#login-button")

        # Verify successful login
        assert page.locator("div.inventory_list").is_visible(), "Login failed"

        context.close()
        browser.close()

def test_responsive_design():
    ensure_traces_directory()
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=traces_path)
        page = context.new_page()
        resolutions = [
            {"width": 1920, "height": 1080},  # Desktop
            {"width": 768, "height": 1024},   # Tablet
            {"width": 375, "height": 667}    # Mobile
        ]

        for res in resolutions:
            page.set_viewport_size(res)
            page.goto("https://www.saucedemo.com/")
            assert page.locator("div.login_wrapper").is_visible(), f"Login wrapper not visible for resolution {res}"

        context.close()
        browser.close()

def test_broken_links():
    ensure_traces_directory()
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=traces_path)
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")
        verify_broken_links(page)

        context.close()
        browser.close()

def test_performance_metrics():
    ensure_traces_directory()
    traces_path = os.path.join(os.path.dirname(__file__), "..", "traces", "performance.har")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_har_path=traces_path)
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")

        metrics = page.evaluate("() => window.performance.timing")
        load_time = metrics["loadEventEnd"] - metrics["navigationStart"]
        assert load_time < 5000, f"Website took too long to load: {load_time}ms"

        context.close()
        browser.close()

if __name__ == "__main__":
    #test_website_loads()
    #test_navigation_links()
    #test_login_functionality()
    #test_responsive_design()
    #test_broken_links()
    #test_performance_metrics()

    pytest.main([__file__, "--html=report.html", "--self-contained-html"])
