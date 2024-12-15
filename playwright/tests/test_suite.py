from playwright.sync_api import sync_playwright
import os
import pytest


def test_website_loads():
    # Ensure traces directory exists
    if not os.path.exists("traces"):
        os.makedirs("traces")
    with sync_playwright() as p:
        browser = p.chromium.launch(traces_dir="traces")
        page = browser.new_page()
        response = page.goto("https://www.saucedemo.com/")
        assert response.status == 200, "Failed to load the website"
        assert "Swag Labs" in page.title(), "Title is missing or incorrect"
        # Add interaction to generate traces
        page.click("#login-button")
        # Ensure the results page has loaded by checking for an element
        assert page.locator("h3").is_visible(), "Google search results not visible"

        # Optionally, add more checks or interactions if needed
        browser.close()

