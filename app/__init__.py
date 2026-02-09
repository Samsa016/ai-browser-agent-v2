import playwright
browser = playwright.chromium.launch(headless=False)

browser.new_context()