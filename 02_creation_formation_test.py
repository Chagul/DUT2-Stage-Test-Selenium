# coding: utf8
import unittest
import time
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
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select

URL = BASE_URL + NOM_DPT + "/Scolarite"

ACRONYME_FORMATION = "formationtest"


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
        self.driver.get(BASE_URL + "/ScoDoc")

    # Test Creer une formation
    # @expected : La formation se trouve dans le tableau de la liste des formations
    def test_011_create_formation(self):
        driver = self.driver
        global URL
        driver.get(URL)
        driver.find_element_by_id("link-programmes").click()
        URL = driver.current_url
        driver.find_element_by_id("link-create-formation").click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_id("tf_acronyme").send_keys(ACRONYME_FORMATION)
        driver.find_element_by_id("tf_titre").send_keys("TEST")
        driver.find_element_by_id("tf_titre_officiel").send_keys("formation de test")
        driver.find_element_by_id("tf_submit").click()
        driver.get(URL)
        formations = driver.find_elements_by_class_name("acronyme")
        textElementAcronyme = []
        for formation in formations:
            textElementAcronyme.append(formation.text)
        self.assertTrue(ACRONYME_FORMATION in textElementAcronyme)

    # Test : Changement du nom d'une formation
    # @expected : Le nom de la formation est changé sur la page des formations
    def test_012_change_name_formation(self):
        driver = self.driver
        global URL
        driver.get(URL)
        idEditFormation = "edit-formation-" + ACRONYME_FORMATION.replace(" ","-")
        driver.find_element_by_id(idEditFormation).click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_id("tf_acronyme").send_keys(ACRONYME_FORMATION)
        driver.find_element_by_id("tf_submit").click()
        driver.get(URL)
        formations = driver.find_elements_by_class_name("acronyme")
        textElementAcronyme = []
        for formation in formations:
            textElementAcronyme.append(formation.text)
        self.assertTrue(ACRONYME_FORMATION + ACRONYME_FORMATION in textElementAcronyme)
        # Remise du nom à celui de départ
        driver.get(URL)
        idEditFormation = "edit-formation-" + ACRONYME_FORMATION + ACRONYME_FORMATION
        driver.find_element_by_id(idEditFormation).click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_id("tf_acronyme").clear()
        driver.find_element_by_id("tf_acronyme").send_keys(ACRONYME_FORMATION)
        driver.find_element_by_id("tf_submit").click()

    # Test : Création d'une formation avec le même nom qu'une autre déjà existante
    # @expected : La formation n'as pas pu être créée et on arrive donc sur un message d'erreur à la création
    def test_013_same_name_formation(self):
        driver = self.driver
        global URL
        driver.get(URL)
        driver.find_element_by_id("link-create-formation").click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_id("tf_acronyme").send_keys(ACRONYME_FORMATION)
        driver.find_element_by_id("tf_titre").send_keys("TEST")
        driver.find_element_by_id("tf_titre_officiel").send_keys("formation de test")
        driver.find_element_by_id("tf_submit").click()
        try:
            driver.find_element_by_class_name("error-message")
            message_erreur_present = True
        except NoSuchElementException:
            message_erreur_present = False
        self.assertTrue(message_erreur_present)

    # Test : Ajout d'une UE dans la formation
    # @Expected : L'UE est créée et elle apparait désormais dans la liste d'UE de la formation
    def test_014_ajout_UE(self):
        driver = self.driver
        global URL
        driver.get(URL)
        idTitre = "titre-" + ACRONYME_FORMATION.replace(" ", "-")
        driver.find_element_by_id(idTitre).click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_xpath("//a[contains(@href,'ue_create?')]").click()
        driver.find_element_by_id("tf_titre").send_keys("UE TEST")
        driver.find_element_by_id("tf_acronyme").send_keys("TEST")
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        driver.get(URL)
        driver.find_element_by_id(idTitre).click()
        self.wait.until(EC.url_changes(URL))
        self.assertTrue("TEST UE TEST" in driver.page_source)
        driver.get(URL)

    # Test : Ajout d'une matière dans la formation
    # @Expected : La matière est créée et elle apparait désormais sur la page de détail de la formation
    def test_015_ajout_matiere(self):
        driver = self.driver
        global URL
        nomMat = "unematieretest"
        driver.get(URL)
        time.sleep(3)
        idTitre = "titre-" + ACRONYME_FORMATION
        driver.find_element_by_id(idTitre).click()
        self.wait.until(EC.url_changes(URL))
        time.sleep(3)
        driver.find_element_by_xpath("//a[contains(@href,'matiere_create?')]").click()
        driver.find_element_by_id("tf_titre").send_keys(nomMat)
        driver.find_element_by_id("tf_numero").send_keys("1")
        driver.find_element_by_id("tf_submit").click()
        time.sleep(3)
        driver.get(URL)
        driver.find_element_by_id(idTitre).click()
        time.sleep(3)
        self.wait.until(EC.url_changes(URL))
        elements = driver.find_elements_by_xpath("//a[contains(@href,'matiere_edit?')]")
        matIsPresent = False
        for element in elements:
            if element.text == nomMat:
                matIsPresent = True
        self.assertTrue(matIsPresent)

    # Test : Ajout d'un semestre dans la formation
    # @Expected : Le semestre est créé et il apparait désormais dans la table des formations
    def test_016_ajout_Semestre(self):
        driver = self.driver
        global URL
        driver.get(URL)
        idAddSemestre = "add-semestre-" + ACRONYME_FORMATION.replace(" ", "-")
        driver.find_element_by_id(idAddSemestre).click()
        self.wait.until(EC.url_changes(URL))
        driver.find_element_by_name("date_debut").send_keys("01/01/2021")
        driver.find_element_by_name("date_fin").send_keys("30/06/2021")
        driver.find_element_by_name("responsable_id").send_keys("BACH Test (Bach)")
        Select(driver.find_element_by_id("tf_semestre_id")).select_by_value("4")
        driver.find_element_by_id("tf_submit").click()
        self.wait.until(EC.url_changes(URL))
        self.assertTrue(
            "Nouveau semestre créé"
            in driver.find_element_by_class_name("head_message").text
        )
        driver.get(URL)

        self.assertTrue((NOM_DPT.upper() + "-" + "DUT" + "--") in driver.page_source)

    # Test : Dupplique une formation sous une nouvelle version
    # @expected : La formation est dupliquée et à la version "2"
    def test_017_creer_nouvelle_version_formation(self):
        driver = self.driver
        global URL
        driver.get(URL)
        idTitre = "titre-" + ACRONYME_FORMATION
        driver.find_element_by_id(idTitre).click()
        self.wait.until(EC.url_changes(URL))
        tmpurl = driver.current_url
        driver.find_element_by_xpath(
            "//a[contains(@href,'formation_create_new_version?')]"
        ).click()
        self.wait.until(EC.url_changes(tmpurl))
        self.assertTrue("Nouvelle version !" in driver.page_source)
        driver.get(URL)
        elements = driver.find_elements_by_class_name("version")
        versionIsPresent = False
        for element in elements:
            if element.text == "2":
                versionIsPresent = True
        self.assertTrue(versionIsPresent)

    # Test : Supprime une formation après avoir supprimé les semestres qui y sont rattachés
    # @expected : La formation n'apparait plus dans le tableau des formations
    def test_020_delete_formation(self):
        driver = self.driver
        global URL
        driver.get(URL)
        idButtonDelete = "delete-formation-" + ACRONYME_FORMATION
        driver.find_element_by_id(idButtonDelete).click()
        self.wait.until(EC.url_changes(URL))
        tmpURLDelete = driver.current_url
        listeSemestres = driver.find_elements_by_xpath(
            "//a[contains(@href, 'formsemestre_status?')]"
        )
        for semestre in listeSemestres:
            semestre.click()
            self.wait.until(EC.url_changes(URL))
            driver.find_element_by_xpath(
                "(//a[contains(text(),'Semestre')])[2]"
            ).click()
            driver.find_element_by_xpath(
                "//a[contains(@href, 'formsemestre_delete?')]"
            ).click()
            self.wait.until(EC.url_changes(URL))
            driver.find_element_by_id("tf_submit").click()
            time.sleep(2)
            driver.find_element_by_xpath("//input[@value='OK']").click()
            driver.get(tmpURLDelete)
        driver.find_element_by_xpath(
            "//input[@value='Supprimer cette formation']"
        ).click()
        driver.get(URL)
        formations = driver.find_elements_by_class_name("version")
        formationDelete = True
        for formation in formations:
            if "1" in formation.text:
                formationDelete = False
        self.assertTrue(formationDelete)

    # def test_create_module(self):
    #    driver = self.driver
    #    element = driver.find_element_by_name("TESTDPT")

    # ferme la fenetre à chaque fin de test
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    deleteDepartement.main()
    createDepartement.main()
    creationSiteDepartement.main()

    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="02_creation_formation_test",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
