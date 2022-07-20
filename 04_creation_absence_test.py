import unittest
import time
import urllib.parse as urlparse
import subprocess
import HtmlTestRunner
import createDepartement
import creationSiteDepartement
import deleteDepartement
from setting import (
    SCODOC_ADMIN_ID,
    SCODOC_ADMIN_PASS,
    BASE_URL,
    NOM_DPT,
    LINK_SCODOC_SERVER,
    BASE_NOT_SECURED_URL,
    NAVIGATEUR,
)
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.select import Select

URL = BASE_URL + NOM_DPT + "/Scolarite"
NOM_ETU = "Semestre11"
PRENOM_ETU = "EtudiantNumero1"
dateDebutAbsenceNonJustifiee = "31/05/2021"
dateDebutAbsenceJustifiee = "25/05/2021"


class PythonOrgSearch(unittest.TestCase):
    # Permet de se connecter et se remettre sur la page d'accueil avant chaque test
    def setUp(self):
        if NAVIGATEUR == "firefox":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
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
        global URL
        self.driver.get(URL)

    def test_010_trouver_etudiant(self):
        driver = self.driver
        global URL
        self.driver.get(BASE_URL + NOM_DPT + "/Scolarite")
        element = self.driver.find_element_by_id("in-expnom")
        element.send_keys(NOM_ETU)
        element.submit()
        self.wait.until(EC.url_changes(URL))
        URL = driver.current_url
        self.assertTrue(NOM_ETU.upper() in driver.page_source)

    # Test : creer une absence non justifiée
    # @expected : La fiche étudiante est incrémentée avec le nombre d'absence injustifiée correspondant
    def test_020_ajout_absence_non_justifiee(self):
        driver = self.driver
        global URL
        driver.find_element_by_id("add-absence").click()
        driver.find_element_by_name("datedebut").send_keys(dateDebutAbsenceNonJustifiee)
        driver.find_element_by_id("butsubmit").submit()
        time.sleep(1)
        self.assertTrue(
            "Ajout de 2 absences <b>NON justifiées</b>" in driver.page_source
        )

        driver = self.driver
        driver.find_element_by_link_text("Liste").click()
        self.assertTrue("2 absences non justifiées:" in driver.page_source)

    # def test_modification_liste_absence_non_justifiee(self):
    #    driver = self.driver
    #    driver.find_element_by_link_text("Liste").click()
    #    self.assertTrue("2 absences non justifiées:" in driver.page_source)

    # Test pour ajouter deux absences justifiées
    # @expected : La fiche d'information de l'étudiant concerné à son compteur d'absence augmenté de 2
    def test_021_ajout_absence_justifiee(self):
        driver = self.driver
        global URL
        driver.find_element_by_id("add-absence").click()
        driver.find_element_by_name("datedebut").send_keys(dateDebutAbsenceJustifiee)
        driver.find_element_by_name("estjust").click()
        driver.find_element_by_id("butsubmit").submit()
        time.sleep(1)
        self.assertTrue("Ajout de 2 absences <b>justifiées</b>" in driver.page_source)
        driver = self.driver
        driver.find_element_by_link_text("Liste").click()
        self.assertTrue("2 absences justifiées:" in driver.page_source)

    # def test_modification_liste_absence_justifiee(self):
    #    driver = self.driver
    #    driver.find_element_by_link_text("Liste").click()
    #    self.assertTrue("2 absences justifiées:" in driver.page_source)

    # Test Justification d'une absence non justifiée
    # @expected : Le champs des absences non justifiées diminue et celui des justifiés augmente du nombre d'absence
    def test_022_ajout_justification(self):
        driver = self.driver
        global URL
        driver.find_element_by_id("justify-absence").click()
        driver.find_element_by_name("datedebut").send_keys(dateDebutAbsenceJustifiee)
        driver.find_element_by_name("description").send_keys("Un test selenium")
        driver.find_element_by_xpath("//input[@value='Envoyer']").click()
        self.wait.until(EC.url_changes(URL))
        self.assertTrue("Ajout de 2 <b>justifications</b>" in driver.page_source)
        driver = self.driver
        driver.find_element_by_link_text("Liste").click()
        self.assertTrue("2 absences justifiées:" in driver.page_source)
        self.assertTrue("absences non justifiées:" in driver.page_source)

    # def test_modification_liste_ajout_justification(self):
    #    driver = self.driver
    #    driver.find_element_by_link_text("Liste").click()
    #    self.assertTrue("4 absences justifiées:" in driver.page_source)
    #    self.assertTrue("absences non justifiées:" not in driver.page_source)

    # Test Suppression des absences pour un élève
    # @expected : Les compteurs d'absences sont remplacés par "Pas d'absences"
    def test_024_supprimer_absence(self):
        driver = self.driver
        global URL
        driver.find_element_by_id("delete-absence").click()
        driver.find_element_by_name("datedebut").send_keys(dateDebutAbsenceJustifiee)
        driver.find_element_by_xpath("//input[@value='Supprimer les absences']").click()
        self.wait.until(EC.url_changes(URL))
        self.assertTrue("Annulation sur 2 demi-journées " in driver.page_source)
        driver.find_element_by_id("delete-absence").click()
        driver.find_element_by_name("datedebut").send_keys(dateDebutAbsenceNonJustifiee)
        driver.find_element_by_xpath("//input[@value='Supprimer les absences']").click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_id("display-list-absence").click()
        self.assertTrue("Pas d'absences justifiées" in driver.page_source)
        self.assertTrue("Pas d'absences non justifiées" in driver.page_source)

    # def test_modification_liste_supression_absence(self):
    #    driver = self.driver
    #    driver.find_element_by_link_text("Liste").click()
    #    self.assertTrue("2 absences justifiées:" in driver.page_source)
    #    self.assertTrue("absences non justifiées:" not in driver.page_source)

    # ferme la fenetre
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
        "test_scenario2_formation.py",
    ]
    process = subprocess.Popen(cmdProcess)
    process.wait()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="04_Absences_tests",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
