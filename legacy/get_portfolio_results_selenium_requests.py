"""
pip install selenium, requests,pandas, pendulum, xvfbwrapper
install firefox & Xvfb
"""
import os
from io import StringIO
import logging

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pendulum

logger = logging.getLogger(__name__)


DE_GIRO_WEB_TRADER_DOMAIN_URL = "https://trader.degiro.nl"
login_url = f"{DE_GIRO_WEB_TRADER_DOMAIN_URL}/login"

de_giro_credentials = {
    "username": os.getenv("de_giro_username"),
    "password": os.getenv("de_giro_password"),
    "account_id": os.getenv("de_giro_account_id"),

}
DATE_STING_FORMAT = "%d/%m/%Y"

if os.getenv('no_browser_gui'):
    from xvfbwrapper import Xvfb

    vdisplay = Xvfb()
    vdisplay.start()

firefox_drive_path = "../gecko_driver/geckodriver"
s = Service(firefox_drive_path)
browser = webdriver.Firefox(service=s)

browser.get(login_url)
browser.find_element(by=By.ID, value="username").send_keys(de_giro_credentials['username'])
browser.find_element(by=By.ID, value="password").send_keys(de_giro_credentials['password'])
browser.find_element(by=By.NAME, value="loginButtonUniversal").click()

# headers = {
# "User-Agent":
#     "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# }
#
# s = requests.session()
# s.headers.update(headers)
# for cookie in browser.get_cookies():
#     c = {cookie['name']: cookie['value']}
#     s.cookies.update(c)
#
#
# session_id = [cookie['value'] for cookie in browser.get_cookies() if cookie.get('name') == "JSESSIONID"].pop()
#
#
# internal_account_number = de_giro_credentials['account_id']
# session_id = s.cookies['JSESSIONID']
# todays_date = pendulum.now("UTC").date().strftime(DATE_STING_FORMAT)
#
# portfolio_report_csv_url = \
#     f"{DE_GIRO_WEB_TRADER_DOMAIN_URL}/reporting/secure/v3/positionReport/csv?intAccount={internal_account_number}&sessionId={session_id}&country=NL&lang=nl&toDate={todays_date}"
#
# response = s.get(portfolio_report_csv_url)
#
# portfolio_result_df = pd.read_csv(StringIO(str(response.content.decode('utf-8'))))
#
#
#

# TODO: see how the header looks like with https://pypi.org/project/selenium-wire/
portfolio_path = "https://trader.degiro.nl/trader/#/portfolio"
browser.get(portfolio_path)

xpath_export_button =\
   "/html/body/div[1]/div/div[1]/div[2]/main/div[1]/section/div/section/div[1]/div/header/div/button/i"
browser.find_element(by=By.XPATH, value=xpath_export_button).click()

xpath_csv_download = "/html/body/div[3]/div/div/div[2]/div/div[2]/a[3]"
browser.find_element(by=By.XPATH, value=xpath_csv_download).click()

internal_account_number = "1378968"
session_id = "24FE65A0EEA137D06B26972627F7445C.prod_b_125_2"
todays_date = "15/01/2022"

portfolio_report_csv_url = \
    f"https://trader.degiro.nl/reporting/secure/v3/positionReport/csv?intAccount={internal_account_number}&sessionId={session_id}&country=NL&lang=nl&toDate={todays_date}"

headers = {
"User-Agent":
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
s = requests.session()
s.headers.update(headers)
for cookie in browser.get_cookies():
    c = {cookie['name']: cookie['value']}
    s.cookies.update(c)

response = s.get(portfolio_report_csv_url)

if os.getenv('no_browser_gui'):
    vdisplay.stop()
