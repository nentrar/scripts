# Selenium script for clone & link Zephyr Test issues

If You are using Zephyr for JIRA and have to clone & link multiple "Test" issues, the script will do that job for You. 
It is written in Selenium so it will be "clicking" in the browser.

You just have to prepare set of "Test" issues and fill the config.json file:

```
{
  "JIRA": {
    "USER_LOGIN": "user",
    "USER_PASSWORD": "password",
    "JIRA_LOGIN_URL": "https://jira.com/login.jsp"
  },
  "NUMBERS": {
    "INTEGRATION": [],
    "PERFORMANCE": []
  },
  "ISSUES": {
    "INTEGRATION": [
      {
        "ISSUE_ID": "PROJECT-1111",
        "ISSUE_NAME": "Name of the TEST issue"
      },
      {
        "ISSUE_ID": "PROJECT-2222",
        "ISSUE_NAME": "Name of the TEST issue"
      }
    ],
    "PERFORMANCE": [
      {
        "ISSUE_ID": "PROJECT-3333",
        "ISSUE_NAME": "Name of the TEST issue"
      }
    ]
  },
  "CLONE": {
    "INTEGRATION": true,
    "PERFORMANCE": true
  }
}
```
* In **JIRA**: add Your credentials and url to JIRA login page.
* In **NUMBERS**: add the numbers of "TASK" issues You want "TESTs" to be linked with using Test Scenario's names as a key.
* In **ISSUES**: add information about "TEST" issues divided by Test Scenario's.
* In **CLONE**: add true if You want that Test Scenario to be cloned and false if not.

### IMPORTANT
The Test Scenario "keys" must be the same for each of NUMBERS, ISSUES, CLONE sections. 
