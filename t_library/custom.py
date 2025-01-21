from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utility.read import ConfigReader
from locators import locators
from testdata import data
import os
from datetime import date, datetime

Data = ConfigReader()
config = Data.read_config_values()

driver = webdriver.Chrome()

def Key_Launch_Browser():
    url = config.get("URL","base_url")+config.get("URL","issue_url")
    driver.get(url)
    driver.maximize_window()

def Key_Login_To_Jira():
    Key_Find_Element(driver, 10, By.XPATH, locators.Username_txtbx).send_keys(config.get("CREDS","username"))
    Key_Find_Element(driver, 10, By.XPATH, locators.Password_txtbx).send_keys(config.get("CREDS","password"))
    Key_Find_Element(driver, 10, By.XPATH, locators.SignIn_btn).click()
    execpted = data.expected_dashboard_text
    actual = Key_Find_Element(driver, 10, By.XPATH, locators.Dashboard_txt).text
    assert execpted == actual

def Key_Take_Screenshot():
    now_time = datetime.now().strftime("%I-%M-%p")
    status_folder = create_folder_today("./snapshots")
    screenshots_folder = os.path.join(".",status_folder)
    Key_Find_Element(driver, 10, By.XPATH, locators.Pichart_img).screenshot(f"{screenshots_folder}/snapshot1_name_{now_time}.png")
    Key_Find_Element(driver, 10, By.XPATH, locators.Pichart_img).screenshot(f"{screenshots_folder}/snapshot2_name_{now_time}.png")

def Key_Find_Element(driver, wait_time, locator_type, locator_value, condition_type="presence"):
    """
    A reusable function for dynamic waits in Selenium.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_time (int): Maximum wait time (in seconds).
        locator_type (By): The type of locator (e.g., By.XPATH, By.ID, etc.).
        locator_value (str): The value of the locator.
        condition_type (str): The condition to wait for.
                             Options: "presence", "visibility", "clickable"

    Returns:
        WebElement: The located web element if the condition is met.
    """
    try:
        wait = WebDriverWait(driver, wait_time)

        if condition_type == "presence":
            return wait.until(EC.presence_of_element_located((locator_type, locator_value)))
        elif condition_type == "visibility":
            return wait.until(EC.visibility_of_element_located((locator_type, locator_value)))
        elif condition_type == "clickable":
            return wait.until(EC.element_to_be_clickable((locator_type, locator_value)))
        else:
            raise ValueError("Invalid condition_type. Use 'presence', 'visibility', or 'clickable'.")

    except Exception as e:
        print(f"Error: {e}")
        return None

def create_folder_today(folder_path):
    today = date.today().strftime("%d-%m-%Y")
    folder_name = f"Status_{today}"
    full_folder_path = os.path.join(folder_path, folder_name)
    if not os.path.exists(full_folder_path):
        os.mkdir(full_folder_path)
        print(f"Folder '{full_folder_path}' created successfully.")
    else:
        print(f"Folder '{full_folder_path}' already exists.")

    return full_folder_path

