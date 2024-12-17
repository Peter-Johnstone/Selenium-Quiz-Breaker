# Selenium-Quiz-Breaker

**Quiz Automation in CSCI308**

## Overview

The **Selenium-Quiz-Breaker** is a Python-based automation tool developed for the Bucknell CSCI308 course that allows the user to automate quiz password attempts on Moodle. 

Leveraging Selenium WebDriver, the script navigates through various states of the Moodle quiz interface, handling scenarios such as initial attempts, re-attempts, and continuing previous attempts. Additionally, it records each password attempted, aiding in tracking and analysis.

## Features

- **Automated Button Handling:** Detects and interacts with "Attempt quiz", "Re-attempt quiz", and "Continue your attempt" buttons.
- **Password Management:** Automates the entry and submission of passwords from a provided list.
- **Logging:** Records each attempted password to a `tried_passwords.txt` file for tracking purposes.
- **Performance Optimizations:** Utilizes headless browser mode and other optimizations to enhance execution speed.
- **Robust Error Handling:** Gracefully handles exceptions and ensures the script continues running smoothly.
