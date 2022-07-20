# coding: utf8
import unittest
import time
import subprocess
import HtmlTestRunner
import createDepartement
import creationSiteDepartement
import deleteDepartement
import suppressionSiteDepartement
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select


class PythonOrgSearch(unittest.TestCase):
    # Permet de se connecter et se remettre sur la page d'accueil avant chaque test
    def setUp(self):
        if NAVIGATEUR == "firefox":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        self.driver.get(
            "https://"
            + SCODOC_ADMIN_ID
            + ":"
            + SCODOC_ADMIN_PASS
            + "@"
            + BASE_NOT_SECURED_URL
            + "force_admin_authentication"
        )
        self.driver.get(BASE_URL)

    # Test : Verification de la connexion admin effective
    # @expected : "Bonjour admin" est présent sur la page d'accueil
    def test_01_connexion_admin(self):
        driver = self.driver
        self.assertTrue("admin" in driver.page_source)

    # Test : Creer un département
    # @expected : Le département est présent sur la page d'accueil
    def test_02_create_departement(self):
        driver = self.driver
        driver.get(BASE_URL + "/scodoc_admin")
        time.sleep(2)
        select = Select(driver.find_element_by_id("create-dept"))
        select.select_by_visible_text(NOM_DPT)
        driver.find_element_by_id("create-dept").submit()
        time.sleep(1)
        driver.find_element_by_id("tf_submit").click()
        driver.get(BASE_URL)
        self.assertTrue(NOM_DPT in driver.page_source)

    # Test : Suppresion d'un département, puis lancement d'un script coté serveur pour supprimer sa base de données
    # @expected : Le département n'apparait plus sur la page d'accueil
    def test_03_delete_departement(self):
        driver = self.driver
        driver.get(BASE_URL + "/scodoc_admin")
        select = Select(driver.find_element_by_id("delete-dept"))
        select.select_by_visible_text(NOM_DPT)
        driver.find_element_by_id("delete-dept").submit()
        driver.get(BASE_URL)
        self.assertTrue(NOM_DPT not in driver.page_source)

    # ferme la fenetre à chaque fin de test
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    deleteDepartement.main()
    createDepartement.main()
    suppressionSiteDepartement.main()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="01_création_département",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
