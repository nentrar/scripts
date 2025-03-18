from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import *
import datetime
import json
from selenium.webdriver.firefox.options import Options

#options = Options()
#options.headless = True

# Driver variable to open a Firefox browser
driver = webdriver.Firefox()

# Variables from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

JIRA_URL = config['JIRA']['JIRA_LOGIN_URL']
JIRA_USER_LOGIN = config['JIRA']['USER_LOGIN']
JIRA_USER_PASSWORD = config['JIRA']['USER_PASSWORD']


# This part open Jira webpage and log in with given credentials
def jira_login(jira_url, jira_user_login, jira_user_pass):
    print "Start logging to Jira service..."
    driver.get(jira_url)
    driver.maximize_window()
    assert "Log in - JIRADC(EE Jira 7.6)" in driver.title
    login_form = driver.find_element_by_id("login-form-username")
    login_form.send_keys(jira_user_login)
    pass_form = driver.find_element_by_id("login-form-password")
    pass_form.send_keys(jira_user_pass)
    login_button = driver.find_element_by_id("login-form-submit")
    login_button.click()
    print str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Login successfull!"


def clone_jira(cloned_issue, cloned_issue_name, number):
    driver.get("https://jiradc.int.net.nokia.com/browse/" + cloned_issue)
    driver.find_element_by_xpath("//span[contains(text(),'Clone')]").click()

    wait = ui.WebDriverWait(driver, 30)
    wait.until(
        lambda driver: driver.find_element_by_xpath("//h2[contains(text(),'Clone issue: " + cloned_issue + "')]"))

    driver.find_element_by_xpath("//input[@id='summary']").send_keys(cloned_issue_name)

    driver.find_element_by_id("clone-issue-submit").click()

    wait.until(
        lambda driver: driver.find_element_by_xpath("//span[@data-name='Created' and child::time[text()='Just now']]"))

    actions = ActionChains(driver)
    for _ in range(2):
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(1)

    driver.find_element_by_id("add-links-link").click()

    wait.until(lambda driver: driver.find_element_by_xpath("//h2[text()='Link']"))
    str_number = str(number)
    jira = "NIAARD-" + str_number

    driver.find_element_by_id("jira-issue-keys-textarea").send_keys(jira)
    actions.send_keys(Keys.ENTER).perform()

    driver.find_element_by_xpath("//input[@value='Link']").click()

    wait.until(
        lambda driver: driver.find_element_by_xpath("//a[@class='issue-link link-title' and text()='" + jira + "']"))

    print str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Jira " + jira + " was successfully linked!"



# This part will go through numbers and for each one clone jira out of source and link issue to it
def jira_clone_link(cloned_issue, cloned_issue_name, numbers):

    for number in numbers:

        try:

            clone_jira(cloned_issue, cloned_issue_name, number)

        except (NoSuchElementException, ElementNotVisibleException, TimeoutException, UnexpectedAlertPresentException) as e:
            print "---------------------------------"
            print str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Oops! The jira is working very slow at the moment and webdriver could not find an xpath. Trying again with:"
            print number

            try:
                clone_jira(cloned_issue, cloned_issue_name, number)

            except (NoSuchElementException, ElementNotVisibleException, TimeoutException, UnexpectedAlertPresentException) as e:

                print str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Oops! The jira is still working very slow at the moment and webdriver could not find an xpath. Trying again."
                clone_jira(cloned_issue, cloned_issue_name, number)

            print "---------------------------------"

    print str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " All issues related to '"+cloned_issue_name+"' has been cloned with success!"

# Next function takes data from json. At first check the "TEST_ON" section for true.
# For those takes the key and then execute the clone_jira_link function for the values of the key in "ISSUES" section
# taking key connected numbers from "NUMBERS" section.

def automatic_clone(config_file):
    for key in config_file["CLONE"]:
        if config_file["CLONE"][key] == True:
            jira_numbers = config_file["NUMBERS"][key]
            tests = config_file["ISSUES"][key]
            for n in range(len(tests)):
                jira_issue = tests[n]["ISSUE_ID"]
                jira_name = tests[n]["ISSUE_NAME"]
                jira_clone_link(jira_issue, jira_name, jira_numbers)




# Below is actual program to clone & link issues.
# Starting with a login
jira_login(JIRA_URL, JIRA_USER_LOGIN, JIRA_USER_PASSWORD)
#Automatic clone based on json config file
automatic_clone(config)
# Closing driver at the end
driver.close()




