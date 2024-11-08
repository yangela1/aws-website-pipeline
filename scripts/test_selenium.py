from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the Chrome WebDriver with the correct path to chromedriver
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')  # Update this path

# Open your HTML page (local file path or hosted URL)
driver.get("file:///var/www/html/index.html")  # Change this to the path of your HTML file

# Wait for the page to load (optional, to give the page time to load)
time.sleep(2)

# Check if the iframe is loaded correctly
try:
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    if iframe.is_displayed():
        print("Iframe is displayed correctly.")
    else:
        print("Iframe is not displayed.")
except Exception as e:
    print("Iframe not found:", e)

# Check if the link is displayed correctly
try:
    link = driver.find_element(By.LINK_TEXT, "Link to view my resume")
    if link.is_displayed():
        print("Link is visible.")
    else:
        print("Link is not visible.")
except Exception as e:
    print("Link not found:", e)

# Optionally, validate any other elements (like the header or body content)
try:
    header = driver.find_element(By.TAG_NAME, "h1")
    if header.is_displayed():
        print(f"Header text: {header.text}")
    else:
        print("Header not found.")
except Exception as e:
    print("Header not found:", e)

# Close the browser after the test
driver.quit()
