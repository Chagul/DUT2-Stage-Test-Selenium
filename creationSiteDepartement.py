# coding: utf8
import unittest
import time
import subprocess
import HtmlTestRunner
from setting import (
    SCODOC_ADMIN_ID,
    SCODOC_ADMIN_PASS,
    BASE_URL,
    NOM_DPT,
    LINK_SCODOC_SERVER,
    BASE_NOT_SECURED_URL,
    NAVIGATEUR,
)
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select

URL = BASE_URL + NOM_DPT + "/Scolarite"

ACRONYME_FORMATION = "FormationTEST"


def main():
    if NAVIGATEUR == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
    driver.get(
        "https://"
        + SCODOC_ADMIN_ID
        + ":"
        + SCODOC_ADMIN_PASS
        + "@"
        + BASE_NOT_SECURED_URL
        + "force_admin_authentication"
    )
    driver.get(BASE_URL + "scodoc_admin")
    time.sleep(2)
    try:
        select = Select(driver.find_element_by_id("create-dept"))
        select.select_by_visible_text(NOM_DPT)
        driver.find_element_by_id("create-dept").submit()
        time.sleep(1)
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        driver.close()
    except NoSuchElementException:
        driver.close()