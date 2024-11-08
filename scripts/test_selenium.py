from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your ChromeDriver
chromedriver_path = '/usr/local/bin/chromedriver'  # Update this path if needed

# Set up the ChromeDriver service
service = Service(chromedriver_path)

# Set up the Chrome WebDriver using the service
driver = webdriver.Chrome(service=service)

# Open your HTML page (local file path or hosted URL)
driver.get("file:///var/www/html/index.html")  # Ensure this path is correct

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
