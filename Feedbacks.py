from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver for Firefox
driver = webdriver.Firefox()

# Open the Groover website
driver.get("https://groover.co/en/")

# Wait for the page to load
time.sleep(2)

# Click the login button using CSS Selector
login_button_css = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='loginLink']")
login_button_css.click()

# Wait for the login page to load
time.sleep(2)

# Enter email and password
email_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormEmailInputField']")
email_input.send_keys("aspenjadeartist@gmail.com")  # Replace with your email

password_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormPasswordInputField']")
password_input.send_keys("Scrapy*11")  # Replace with your password

# Press Enter to log in
password_input.send_keys(Keys.RETURN)

# Click the login submit button
login_submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='loginFormSubmitCTA']")
login_submit_button.click()
time.sleep(5)

# List of songs to scrape feedback for
songs = ['BEFORE', 'Obsessed', 'INFINITE', 'Searching', 'Alternate Universes', 'Infinite']

# Open CSV file for writing
with open('song_feedback.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write the header row
    csv_writer.writerow(['Feedback', 'Name', 'Type', 'Song'])  

    def extract_feedbacks(song_name):
        # Find all feedback elements
        feedback_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tw-relative tw-overflow-hidden tw-overflow-ellipsis tw-whitespace-nowrap']/span"))
        )

        # Find all name elements
        name_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'desktopDisplay')]//span[contains(@class, 'tw-ellipsis') and not(contains(., 'Add the requested files'))]"))
        )

        # Find all type elements
        type_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'status')]/span"))
        )

        # Extract feedback, names, and types
        feedbacks = [feedback.text for feedback in feedback_elements if feedback.text.strip() != '']
        names = [name.text for name in name_elements if name.text.strip() != '']
        types = [type_elem.text for type_elem in type_elements if type_elem.text.strip() != '']

        # Write feedbacks, names, and types to CSV
        for i in range(len(feedbacks)):
            feedback = feedbacks[i]
            name = names[i] if i < len(names) else "No name available"
            feedback_type = types[i] if i < len(types) else "No type available"

            # Process feedback type
            if feedback_type == "Feedback":
                feedback_type = "Fail"
            elif feedback_type == "Promise to share":
                feedback_type = "Success"
            else:
                feedback_type = "N/A"

            # Write to CSV
            csv_writer.writerow([feedback, name, feedback_type, song_name])

    # Navigate to each song and scrape feedback
    for song in songs:
        # Navigate to "My Campaigns"
        my_campaigns_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='bandTopNavigationCampaignsCTA']"))
        )
        my_campaigns_link.click()
        time.sleep(5)

        # Locate and click on the song
        song_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{song}']"))
        )
        song_element.click()
        time.sleep(5)

        # Loop through pages and extract feedbacks
        while True:
            extract_feedbacks(song)

            # Locate the "Next Page" button
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Next Page']"))
                )
                next_button.click()
                time.sleep(4)  # Wait for the next page to load
            except Exception:
                break  # Exit loop if "Next Page" button is not found

# Close the WebDriver
driver.quit()
