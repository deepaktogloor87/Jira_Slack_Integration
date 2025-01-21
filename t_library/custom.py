import glob
import shutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
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
today = date.today().strftime("%d-%m-%Y")

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
    Key_Find_Element(driver, 10, By.XPATH, locators.SubUnit_img).screenshot(f"{screenshots_folder}/SubUnit_img_{now_time}.png")
    Key_Find_Element(driver, 10, By.XPATH, locators.TimeAtWork_img).screenshot(f"{screenshots_folder}/TimeAtWork_img_{now_time}.png")

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
    delete_folders_with_date(folder_path)
    folder_name = today
    full_folder_path = os.path.join(folder_path, folder_name)
    if not os.path.exists(full_folder_path):
        os.mkdir(full_folder_path)
        print(f"Folder '{full_folder_path}' created successfully.")
    else:
        print(f"Folder '{full_folder_path}' already exists.")

    return full_folder_path


def delete_folders_with_date(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Loop through all subfolders in the specified path
        for folder_name in os.listdir(folder_path):
            folder_full_path = os.path.join(folder_path, folder_name)

            # Check if the folder name matches the date format
            try:
                folder_date = datetime.strptime(folder_name, "%d-%m-%Y").date()
                current_date = datetime.now().date()

                # If the folder date is older than today, delete the folder
                if folder_date < current_date:
                    shutil.rmtree(folder_full_path)
                    print(f"Deleted folder: {folder_full_path}")
                else:
                    print(f"Folder is from today or a future date. Not deleting: {folder_full_path}")
            except ValueError:
                # If the folder name doesn't match the date format, skip it
                print(f"Skipping folder with non-date name: {folder_name}")
    else:
        print(f"Folder path does not exist: {folder_path}")

def Key_Upload_Status_Files_To_Slack():
    base_folder_path = "./snapshots"
    slack_token = config.get("SLACK","token")  # Replace with your actual Slack Bot Token
    channel_id = config.get("SLACK","channel")

    # Initialize Slack client
    client = WebClient(token=slack_token)

    # Get today's date
    today_date = datetime.now().strftime("%d-%m-%Y")

    # Construct the folder path
    folder_path = os.path.join(base_folder_path, today_date)

    # Heading for the Slack message
    heading = f"*STATUS FOR THE DAY {today_date}* ✅️"

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    # Use glob to find all PNG files in the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))

    if not png_files:
        print(f"No PNG files found in folder: {folder_path}")
        return

    # Upload each PNG file to Slack
    for file_path in png_files:
        try:
            # Use client.files_upload_v2() for better stability
            response = client.files_upload_v2(
                channel=channel_id,
                initial_comment=heading,
                file=file_path
            )
            print(f"Uploaded file: {file_path} to Slack. File ID: {response['file']['id']}")
        except SlackApiError as e:
            print(f"Error uploading file {file_path}: {e.response['error']}")


