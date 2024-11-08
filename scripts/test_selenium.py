from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time  # Import time for sleep functionality

# Get the path to the Chrome binary
chrome_bin_path = os.getenv("CHROME_BIN")

# Set up Chrome options
options = Options()
options.binary_location = chrome_bin_path

# Configure Chrome to run in headless mode (no UI)
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")  # Prevents errors related to sandboxing in some environments
options.add_argument("--disable-dev-shm-usage")  # Avoids issues with shared memory in Docker and AWS environments
options.add_argument("--remote-debugging-port=9222")  # Optional for debugging, might help in some cases

# Set up the Chrome WebDriver using the options
driver = webdriver.Chrome(options=options)

# Open the local HTML file (make sure the path is correct)
driver.get("file:///var/www/html/index.html")  # Adjust the path as needed

# Wait for the page to load (optional, to give the page time to load)
time.sleep(2)

# Check if the link is displayed correctly
try:
    link = driver.find_element(By.LINK_TEXT, "Link to view my resume")
    if link.is_displayed():
        print("Link is visible.")
    else:
        print("Link is not visible.")
except Exception as e:
    print("Link not found:", e)

# Close the browser after the test
driver.quit()
