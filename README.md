**Sprint 8: Urban Routes Automation
Natalia Molina | Cohort 28**

**📝 Project Description**

This project focuses on the automated end-to-end (E2E) testing of the Urban Routes platform, specifically simulating the taxi-booking workflow. The automation script replicates a real user journey, covering critical business logic and UI interactions:

- Setting pickup and destination addresses.
- Selecting various vehicle categories (service levels).
- Phone number entry and verification.
- Payment method integration (card addition and validation).
- Customizing trip requirements (requesting blankets, tissues, or adding driver notes).
- Completing the final booking request.

**🛠️ Tech Stack & Methodology**
- Language: Python
- Automation Engine: Selenium WebDriver
- Test Framework: PyTest (for test suite organization and execution)
- Design Pattern: Page Object Model (POM) — implemented to ensure code reusability, modularity, and easy maintenance.
- Synchronization: Explicit Waits (WebDriverWait and expected_conditions) to handle asynchronous web elements and ensure test stability.
- IDE: PyCharm

**🚀 Execution**
To run the test suite, navigate to the root directory and execute the following command in your terminal:

Bash
pytest test_urban_routes.py -v
