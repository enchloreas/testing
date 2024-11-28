# playwright.config.py
import pytest

def pytest_configure(config):
    # Add configuration for Playwright or custom output paths
    config.addinivalue_line(
        "markers", "playwright: mark a test as a Playwright test"
    )