from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
import time

# Load YouTube links from a JSON file
youtube_links_path = Path("youtube_links.json")
with youtube_links_path.open(mode="r") as file:
    youtube_links = json.load(file)

link_to_get_transcript = "https://tactiq.io/tools/youtube-transcript"

# Function to initialize the Chrome browser
def initialize_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(link_to_get_transcript)
    return driver

# Initialize the driver globally
driver = initialize_chrome()  # Start the browser initially

def download_the_transcript(youtube_link):
    global driver
    try:
        # Add the link to the search bar on the transcript website
        enter_youtube_url = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "yt"))
        )
        enter_youtube_url.clear()
        enter_youtube_url.send_keys(youtube_link)
        enter_youtube_url.send_keys(Keys.ENTER)

        # Wait for the download button to be present and clickable, then click it
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="download"]'))
        )
        time.sleep(1)  # Allow some time for the button to become fully interactable
        download_button.click()

        # Wait a bit before going back to the previous page
        time.sleep(1)
        driver.back()
    
    except Exception as e:
        print(f"There is an issue at {youtube_link} link with error {e}")
        # If the browser window closes, restart the browser (reinitialize)
        if "no such window" in str(e) or "web view not found" in str(e):
            driver.quit()  # Close the current WebDriver instance
            driver = initialize_chrome()  # Reinitialize the driver and navigate back to the transcript page
        return None

    return None

# Process each YouTube link
for link in youtube_links:
    download_the_transcript(link)

# Close the browser at the end of the script
driver.quit()
