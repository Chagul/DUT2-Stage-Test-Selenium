import unittest
import time
import subprocess
import urllib.parse as urlparse
import HtmlTestRunner
import createDepartement
import creationSiteDepartement
import deleteDepartement
from setting import (
    SCODOC_ADMIN_ID,
    SCODOC_ADMIN_PASS,
    BASE_URL,
    BASE_NOT_SECURED_URL,
    LINK_SCODOC_SERVER,
    NOM_DPT,
    SCODOC_ENS_ID,
    SCODOC_ENS_PASS,
    SCODOC_CHEF_ID,
    SCODOC_CHEF_PASS,
    NAVIGATEUR,
)
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.select import Select


URL_ETUDIANT = ""
URL_DECISION = ""


class PythonOrgSearch(unittest.TestCase):
    # Permet de se connecter et se remettre sur la page d'accueil avant chaque test
    def setUp(self):
        if NAVIGATEUR == "firefox":
            self.driver = webdriver.Firefox()
        elif NAVIGATEUR == "chrome":
            self.driver = webdriver.Chrome()
        self.url = BASE_URL + NOM_DPT + "/Scolarite"
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(
            "https://"
            + SCODOC_ADMIN_ID
            + ":"
            + SCODOC_ADMIN_PASS
            + "@"
            + BASE_NOT_SECURED_URL
            + "force_admin_authentication"
        )

    def test_010_etudiantS1_assidu_avec_moy_admis(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID1")
        searchBar.submit()
        time.sleep(5)
        URL_ETUDIANT = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath(
            "//a[contains(@href,'formsemestre_validation_etud_form?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        URL_DECISION = driver.current_url
        driver.find_element_by_id("input-choice-10").click()
        driver.find_element_by_id("subut").click()
        time.sleep(1)
        driver.get(URL_ETUDIANT)
        self.assertTrue("ADM" in driver.find_element_by_class_name("rcp_dec").text)

    def test_020_etudiantS1_non_assidu_avec_moy_semestre_non_valide(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID1")
        searchBar.submit()
        time.sleep(5)
        URL_ETUDIANT = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath(
            "//a[contains(@href,'formsemestre_validation_etud_form?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        URL_DECISION = driver.current_url
        driver.find_element_by_id("input-choice-40").click()
        driver.find_element_by_id("subut").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("ATJ" in driver.find_element_by_class_name("rcp_dec").text)

    def test_030_etudiantS1_assidu_sous_la_moy_semestre_valide(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID4")
        searchBar.submit()
        time.sleep(5)
        URL_ETUDIANT = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath(
            "//a[contains(@href,'formsemestre_validation_etud_form?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        URL_DECISION = driver.current_url
        driver.find_element_by_id("input-choice-30").click()
        driver.find_element_by_id("subut").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("ATB" in driver.find_element_by_class_name("rcp_dec").text)
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath(
            "//a[contains(@href,'formsemestre_validation_etud_form?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        URL_DECISION = driver.current_url
        driver.find_element_by_id("input-choice-580").click()
        driver.find_element_by_id("subut").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("ATB" in driver.find_element_by_class_name("rcp_dec").text)

    def test_040_etudiantS1_non_assidu_sous_la_moy_semestre_valide(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID4")
        searchBar.submit()
        time.sleep(5)
        URL_ETUDIANT = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath(
            "//a[contains(@href,'formsemestre_validation_etud_form?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        URL_DECISION = driver.current_url
        driver.find_element_by_id("input-choice-40").click()
        driver.find_element_by_id("subut").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("ATJ" in driver.find_element_by_class_name("rcp_dec").text)
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath(
            "//a[contains(@href,'formsemestre_validation_etud_form?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        URL_DECISION = driver.current_url
        driver.find_element_by_id("input-choice-580").click()
        driver.find_element_by_id("subut").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("ATB" in driver.find_element_by_class_name("rcp_dec").text)

    def test_050_calcul_automatiqueS2_jury(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        driver.find_element_by_link_text("semestre 2").click()
        self.wait.until(EC.url_changes(url))
        urlTmp = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Jury')]").click()
        driver.find_element_by_link_text("Saisie des décisions du jury").click()
        self.wait.until(EC.url_changes(urlTmp))
        urlTmp = driver.current_url
        driver.find_element_by_partial_link_text("Calcul automatique").click()
        self.wait.until(EC.url_changes(urlTmp))
        urlTmp = driver.current_url
        driver.find_element_by_xpath("//input[@type='submit']").click()
        self.wait.until(EC.url_changes(urlTmp))
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID7")
        searchBar.submit()
        time.sleep(5)
        self.assertTrue("ADM" in driver.find_element_by_class_name("rcp_dec").text)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID10")
        searchBar.submit()
        time.sleep(5)
        self.assertTrue("en cours" in driver.page_source)

    def test_060_declarer_defaillance(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID10")
        searchBar.submit()
        time.sleep(5)
        URL_ETUDIANT = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath("//a[contains(@href,'formDef?')]").click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        input = driver.find_element_by_name("event_date")
        input.clear()
        input.send_keys("11/06/2021")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("Défaillant" in driver.page_source)

    def test_070_declarer_demission(self):
        driver = self.driver
        url = self.url
        driver.get(url)
        searchBar = driver.find_element_by_id("in-expnom")
        searchBar.send_keys("EID10")
        searchBar.submit()
        time.sleep(5)
        URL_ETUDIANT = driver.current_url
        driver.find_element_by_xpath("//a[contains(text(),'Scolarité')]").click()
        driver.find_element_by_xpath("//a[contains(@href,'formDem?')]").click()
        self.wait.until(EC.url_changes(URL_ETUDIANT))
        input = driver.find_element_by_name("event_date")
        input.clear()
        input.send_keys("11/06/2021")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.get(URL_ETUDIANT)
        self.assertTrue("Démission le " in driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    deleteDepartement.main()
    createDepartement.main()
    creationSiteDepartement.main()
    cmdProcess = [
        "./scriptExecution.sh",
        LINK_SCODOC_SERVER,
        NOM_DPT,
        "test_scenario4_formation.py",
    ]
    process = subprocess.Popen(cmdProcess)
    process.wait()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="07_Admission_et_passages_tests",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
