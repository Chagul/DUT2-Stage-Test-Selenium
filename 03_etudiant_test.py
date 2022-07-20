import unittest
import time
import HtmlTestRunner
import subprocess
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
import urllib.parse as urlparse
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.select import Select

URL = BASE_URL + NOM_DPT + "/Scolarite"
nomEtu = "Semestre11"
prenomEtu = "Etudiant1"
nip = "11122234"
domicile = "50 rue de la marmite"
codepostaldomicile = "59000"
paysdomicile = "Lille"


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

    # Test : creer un etudiant et verifie si sa fiche etudiante est creee
    # @expected : A la soumission du formulaire on retrouve la fiche d'information avec le nip (unique) dans la page, on a également un resultat en recherchant l'étudiant
    def test_01_creation_etudiant(self):
        driver = self.driver
        global URL
        driver.find_element_by_id("link-create-student").click()
        self.wait.until(EC.url_changes(URL))
        URL = driver.current_url
        driver.find_element_by_id("tf_nom").send_keys(nomEtu)
        driver.find_element_by_id("tf_prenom").send_keys(prenomEtu)
        driver.find_element_by_id("tf_annee").send_keys("2021")
        driver.find_element_by_id("tf_code_nip").send_keys(nip)
        driver.find_element_by_name("dont_check_homonyms:list").click()
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        self.assertTrue("M. " + prenomEtu + " " + nomEtu.upper() in driver.page_source)
        self.assertTrue(nip in driver.page_source)

    # Test : Creer un étudiant avec un nip qui est déjà présent dans la base Scodoc
    # @expected : La création mène à une page qui affiche "code étudiant dupliqué", l'étudiant n'est pas créé
    def test_02_creation_etudiant_avec_meme_nip(self):
        driver = self.driver
        global URL
        driver.get(URL)
        driver.find_element_by_id("tf_nom").send_keys(nomEtu)
        driver.find_element_by_id("tf_prenom").send_keys(prenomEtu)
        driver.find_element_by_id("tf_annee").send_keys("2021")
        driver.find_element_by_id("tf_code_nip").send_keys(nip)
        driver.find_element_by_name("dont_check_homonyms:list").click()
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        self.assertTrue(
            "Code étudiant (code_nip) dupliqué !"
            in driver.find_element_by_class_name("title-error").text
        )

    # Test Modification de l'adresse étudiant
    # expected : La nouvelle adresse est mise à jour sur la page information de l'étudiant
    def test_03_modification_adresse_etudiant(self):
        driver = self.driver
        global URL
        driver.get(URL)
        element = driver.find_element_by_id("in-expnom")
        element.send_keys(nomEtu)
        element.submit()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_xpath(
            "//a[contains(@href,'formChangeCoordonnees')]"
        ).click()
        time.sleep(1)
        driver.find_element_by_id("tf_domicile").send_keys(domicile)
        driver.find_element_by_id("tf_codepostaldomicile").send_keys(codepostaldomicile)
        driver.find_element_by_id("tf_paysdomicile").send_keys(paysdomicile)
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        self.assertTrue(
            codepostaldomicile in driver.find_element_by_id("student-address").text
        )

    # Test Inscription d'un étudiant dans un semestre
    # @expected :
    def test_04_inscription_etudiant(self):
        driver = self.driver
        global URL
        driver.get(URL)
        element = driver.find_element_by_id("in-expnom")
        element.send_keys(nomEtu)
        element.submit()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_xpath(
            "//a[contains(@href, 'formsemestre_inscription_with_modules_form')]"
        ).click()
        self.wait.until(EC.url_changes(URL))
        try:
            semestres = driver.find_elements_by_xpath(
                "//a[contains(@id,'inscription-semestre-')]"
            )
        except NoSuchElementException:
            self.assertFalse(True)
        semestres[0].click()
        driver.find_element_by_xpath("//input[@value='Inscrire']").click()
        time.sleep(2)
        boutonInscrireIsNotPresent = False
        try:
            driver.find_element_by_partial_link_text("inscrire")
        except:
            boutonInscrireIsNotPresent = True
        self.assertTrue(boutonInscrireIsNotPresent)

    # Test Supprime un étudiant
    # @expected : Lors d'une recherche sur le nom de l'étudiant, aucun résultat apparait
    def test_05_suppresion_etudiant(self):
        driver = self.driver
        urlRecherche = (
            "https://scodoc-dev-iutinfo.univ-lille.fr/ScoDoc/"
            + NOM_DPT
            + "/Scolarite/search_etud_in_dept"
        )
        driver.get(urlRecherche)
        element = driver.find_element_by_name("expnom")
        element.send_keys(nomEtu)
        element.submit()
        time.sleep(1)
        etudid = driver.find_element_by_id("euid")
        url = (
            "https://scodoc-dev-iutinfo.univ-lille.fr/ScoDoc/"
            + NOM_DPT
            + "/Scolarite/etudident_delete?etudid="
            + etudid.text
        )
        driver.get(url)
        time.sleep(1)
        driver.find_element_by_xpath(
            "//input[@value='Supprimer définitivement cet étudiant']"
        ).click()
        driver.get(urlRecherche)
        element = driver.find_element_by_name("expnom")
        element.send_keys(nomEtu)
        element.submit()
        time.sleep(1)
        try:
            element = driver.find_element_by_id("title-no-result")
            self.assertTrue("Aucun résultat" in element.text)
        except:
            self.assertFalse(True)

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
        "test_scenario1_formation.py",
    ]
    process = subprocess.Popen(cmdProcess)
    process.wait()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="03_Etudiant_test",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
