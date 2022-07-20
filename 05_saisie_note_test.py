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
    NOM_DPT,
    SCODOC_ENS_ID,
    SCODOC_ENS_PASS,
    SCODOC_CHEF_ID,
    SCODOC_CHEF_PASS,
    NAVIGATEUR,
    LINK_SCODOC_SERVER,
    BASE_NOT_SECURED_URL,
)
from urllib.parse import parse_qs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support.select import Select

URL_MATIERE = ""
URL_SEMESTRE = ""
URL = BASE_URL + NOM_DPT + "/Scolarite"
PRENOM_ENS = "Ens"
PRENOM_CHEF = "Chef"
isAdmin = True
isChef = False
isEns = False
# Prérequis
class PythonOrgSearch(unittest.TestCase):
    # Permet de se connecter et se remettre sur la page d'accueil avant chaque test
    def setUp(self):
        if NAVIGATEUR == "firefox":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        if isAdmin:
            self.driver.get(
                "https://"
                + SCODOC_ADMIN_ID
                + ":"
                + SCODOC_ADMIN_PASS
                + "@"
                + BASE_NOT_SECURED_URL
                + "force_admin_authentication"
            )
        else:
            self.driver.get(BASE_URL + NOM_DPT + "/Scolarite")
            if isChef:
                self.driver.find_element_by_name("__ac_name").send_keys(SCODOC_CHEF_ID)
                self.driver.find_element_by_name("__ac_password").send_keys(
                    SCODOC_CHEF_PASS
                )
                time.sleep(3)
                self.driver.find_element_by_name("submit").click()
            elif isEns:
                self.driver.find_element_by_name("__ac_name").send_keys(SCODOC_ENS_ID)
                self.driver.find_element_by_name("__ac_password").send_keys(
                    SCODOC_ENS_PASS
                )
                self.driver.find_element_by_name("submit").click()

    # Test : Vérifie s'il y a un semestre en cours
    # @expected  : La class listesems n'est pas vide et contient "Session en cours"
    def test_010_semestre_en_cours(self):
        driver = self.driver
        global URL
        driver.get(URL)
        # time.sleep(1)
        self.assertTrue(
            "Sessions en cours" in driver.find_element_by_class_name("listesems").text
        )

    # Test : Vérifie si une matière existe
    # @expected : Le nom de la matière est présent dans le semestre préalablement testé
    def test_020_matiere_existante(self):
        driver = self.driver
        global URL
        driver.get(URL)
        driver.find_element_by_link_text("semestre 4").click()
        self.wait.until(EC.url_changes(URL))
        matiereExist = False
        try:
            driver.find_element_by_class_name("formsemestre_status_ue")
            global URL_SEMESTRE
            URL_SEMESTRE = driver.current_url
            matiereExist = True
        except NoSuchElementException:
            matiereExist = False
        self.assertTrue(matiereExist)

    #Test : Changement de responsable sur module
    # @expected : Le nom du responsable choisi apparait désormais sur le module concerné 
    def test_030_changement_responsable_sur_module(self):
        driver = self.driver
        isThere = False
        driver.get(URL_SEMESTRE)
        driver.find_element_by_link_text("M4101C").click()
        time.sleep(1)
        global URL_MATIERE
        URL_MATIERE = driver.current_url
        driver.find_element_by_xpath(
            "//a[contains(@href,'edit_moduleimpl_resp?')]"
        ).click()
        self.wait.until(EC.url_changes(URL_MATIERE))
        constructIdResponsable = (
            SCODOC_CHEF_ID.upper()
            + " "
            + PRENOM_CHEF
            + " ("
            + SCODOC_CHEF_ID.lower()
            + ")"
        )
        idInput = driver.find_element_by_name("responsable_id")
        idInput.clear()
        idInput.send_keys(constructIdResponsable)
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        driver.get(URL_MATIERE)
        nomResponsable = driver.find_element_by_id("ens-responsable")
        self.assertTrue(SCODOC_CHEF_ID.lower() in nomResponsable.text.lower())
        global isAdmin
        isAdmin = False
        global isChef
        isChef = True

    # Test : Ajout d'un enseignant comme résponsable d'un module
    # @expected : Le nom de l'enseignant apparait désormais sur la page d'information du module
    def test_031_ajout_enseignant_sur_module(self):
        driver = self.driver
        global URL_MATIERE
        driver.get(URL_MATIERE)
        time.sleep(2)
        driver.find_element_by_partial_link_text("modifier les enseignants").click()
        time.sleep(1)
        constructIDEns = (
            SCODOC_ENS_ID.upper() + " " + PRENOM_ENS + " (" + SCODOC_ENS_ID + ")"
        )
        driver.find_element_by_id("ens_id").send_keys(constructIDEns)
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        driver.get(URL_MATIERE)
        professeurDansModule = driver.find_elements_by_class_name("ens-in-module")
        time.sleep(5)
        professeurString = []
        for professeur in professeurDansModule:
            professeurString.append(professeur.text)
        for professeurS in professeurString:
            if SCODOC_ENS_ID.lower() in professeurS.lower():
                isThere = True
        self.assertTrue(isThere)

    # Test : Création d'une interrogation en tant que chef des études
    # @eexpected : L'interrogation apparait désormais dans ce module
    def test_040_creation_interrogation(self):
        descriptionInterrogation = "Interrogation numero 2"
        driver = self.driver
        global URL_MATIERE
        driver.get(
            "https://"
            + SCODOC_ADMIN_ID
            + ":"
            + SCODOC_ADMIN_PASS
            + "@scodoc-dev-iutinfo.univ-lille.fr/force_admin_authentication"
        )
        # driver.get(BASE_URL)
        # driver.find_element_by_link_text("déconnecter").click()
        # driver.get(BASE_URL)
        # driver.find_element_by_id("name").send_keys(SCODOC_CHEF_ID)
        # driver.find_element_by_id("password").send_keys(SCODOC_CHEF_PASS)
        # driver.find_element_by_id("submit").click()
        driver.get(URL_MATIERE)
        time.sleep(1)
        driver.find_element_by_link_text("Créer nouvelle évaluation").click()
        time.sleep(1)
        driver.find_element_by_name("jour").clear()
        driver.find_element_by_name("jour").send_keys("31/05/2021")
        driver.find_element_by_id("tf_description").send_keys(descriptionInterrogation)
        driver.find_element_by_id("tf_coefficient").send_keys("2")
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        global isChef
        isChef = False
        global isEns
        isEns = True
        self.assertTrue(descriptionInterrogation in driver.page_source)

    # Test Vérifie si une interrogation existe sur un module
    # @expected "Module" est présent dans le "formsemetre"
    def test_050_interro_existante(self):
        driver = self.driver
        global URL_MATIERE
        driver.get(URL_MATIERE)
        time.sleep(1)
        self.assertTrue(
            "Module" in driver.find_element_by_class_name("formsemestre").text
        )

    # Test Entree des notes pour le premier étudiant inscrit à un module
    # @expected : "saisir note" est remplacé par "afficher" sur la page d'information de l'interrogation concernée
    def test_060_entree_note(self):
        driver = self.driver
        global URL_MATIERE
        driver.get(URL_MATIERE)
        driver.find_element_by_class_name("notes_img").click()
        time.sleep(1)
        element = driver.find_element_by_class_name("note")
        element.send_keys("12")
        driver.find_element_by_id("formnotes_submit").click()
        # self.wait.until(EC.url_changes(url))
        self.assertTrue(
            driver.find_element_by_link_text("afficher").text in driver.page_source
        )

    # Test : Ajoute les notes manquante poru les étudiants concernés dans une interrogation
    # @expected : Tout les étudiants on une note
    def test_070_ajout_note_incomplete(self):
        driver = self.driver
        global URL_MATIERE
        driver.get(URL_MATIERE)
        time.sleep(1)
        driver.find_element_by_class_name("notes_img").click()
        elements = driver.find_elements_by_class_name("note")
        for element in elements:
            if element.get_attribute("value") == "":
                element.send_keys(15)
        driver.find_element_by_id("formnotes_submit").click()
        time.sleep(5)
        element = driver.find_element_by_id("in-expnom")
        element.send_keys("SEMESTRE47")
        element.submit()
        time.sleep(5)
        self.assertTrue("12" in driver.find_element_by_class_name("rcp_moy").text)

    # Test : Suppresion des notes pour tout les étudiants concernés dans une interrogation
    # @expected : La moyenne ne s'affiche plus, "afficher" disparait de la page d'information de l'interrogation
    def test_080_suppression_note(self):
        driver = self.driver
        global URL_MATIERE
        driver.get(URL_MATIERE)
        time.sleep(1)
        driver.find_element_by_class_name("notes_img").click()
        time.sleep(1)
        elements = driver.find_elements_by_class_name("note")
        for element in elements:
            element.clear()
            element.send_keys("SUPR")
        driver.find_element_by_id("formnotes_submit").click()
        time.sleep(1)
        interro_non_Presente = False
        try:
            driver.find_element_by_link_text("afficher")
            interro_non_Presente = False
        except NoSuchElementException:
            interro_non_Presente = True
        self.assertTrue(interro_non_Presente)
        global isChef
        isChef = True
        global isEns
        isEns = False

    # Test : SUppression d'une interrogation par le chef des études
    # @expected : L'interrogation n'apparait plus sur le module, les notes sont supprimées également
    def test_090_suppresion_interrogation(self):
        global URL_MATIERE
        descriptionInterrogation = "Interrogation à supprimer"
        driver = self.driver
        driver.get(URL_MATIERE)
        time.sleep(1)
        driver.find_element_by_link_text("Créer nouvelle évaluation").click()
        time.sleep(1)
        driver.find_element_by_name("jour").clear()
        driver.find_element_by_name("jour").send_keys("30/05/2021")
        driver.find_element_by_id("tf_description").send_keys(descriptionInterrogation)
        driver.find_element_by_id("tf_coefficient").send_keys("2")
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        self.assertTrue(descriptionInterrogation in driver.page_source)
        driver.find_element_by_class_name("delete_img").click()
        time.sleep(1)
        driver.find_element_by_id("tf_submit").click()
        # global isAdmin
        # isAdmin = True
        # global isEns
        # isEns = False
        self.assertFalse(descriptionInterrogation in driver.page_source)

    # Test : Suppression d'un enseignant responsable d'un module
    # @expected : L'enseignant n'apparait plus comme responsable dans ce module
    def test_200_suppression_enseignant_sur_module(self):
        driver = self.driver
        driver.get(URL_MATIERE)
        time.sleep(1)
        driver.find_element_by_partial_link_text("modifier les enseignants").click()
        time.sleep(1)
        elements = driver.find_elements_by_link_text("supprimer")
        for element in elements:
            element.click()
            time.sleep(1)
        time.sleep(1)
        driver.get(URL_MATIERE)
        time.sleep(5)
        self.assertTrue(SCODOC_ENS_ID not in driver.page_source)

    # Test : Suppresion du reste des interrogations sans notes
    # @expected Tout les interrogation sans notes sont supprimées
    def test_910_suppresion_interrogation_restante(self):
        driver = self.driver
        driver.get(URL_MATIERE)
        time.sleep(1)
        elements = driver.find_elements_by_xpath(
            "//a[contains(@href,'evaluation_delete?')]"
        )
        while elements:
            elements[0].click()
            driver.find_element_by_id("tf_submit").click()
            self.wait.until(EC.url_changes(URL))
            driver.find_element_by_partial_link_text("Continuer").click()
            self.wait.until(EC.url_changes(URL))
            elements = driver.find_elements_by_xpath(
                "//a[contains(@href,'evaluation_delete?')]"
            )

    # ferme la fenetre et fais du clean up
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    if NAVIGATEUR == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
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
    time.sleep(5)
    driver.get(
        "https://"
        + SCODOC_ADMIN_ID
        + ":"
        + SCODOC_ADMIN_PASS
        + "@"
        + BASE_NOT_SECURED_URL
        + "force_admin_authentication"
    )
    driver.get(BASE_URL + NOM_DPT + "/Scolarite")
    driver.find_element_by_id("link-view-users").click()
    time.sleep(5)
    noms = driver.find_elements_by_class_name("nom_fmt")
    chefCree = False
    ensCree = False
    for nom in noms:
        if nom.text.lower() == SCODOC_CHEF_ID.lower():
            chefCree = True
        if nom.text.lower() == SCODOC_ENS_ID.lower():
            ensCree = True
    if not chefCree:
        time.sleep(2)
        constructValue = "Ens" + NOM_DPT
        driver.find_element_by_id("create-user").click()
        driver.find_element_by_id("tf_nom").send_keys(SCODOC_CHEF_ID)
        driver.find_element_by_id("tf_user_name").send_keys(SCODOC_CHEF_ID)
        driver.find_element_by_id("tf_prenom").send_keys("chef")
        driver.find_element_by_id("tf_passwd").send_keys(SCODOC_CHEF_PASS)
        driver.find_element_by_id("tf_passwd2").send_keys(SCODOC_CHEF_PASS)
        driver.find_element_by_xpath("//input[@value='" + constructValue + "']").click()
        driver.find_element_by_xpath("//input[@name='force:list']").click()
        driver.find_element_by_id("tf_submit").click()
        driver.find_element_by_id("link-view-users").click()
    if not ensCree:
        time.sleep(2)
        constructValue = "Ens" + NOM_DPT
        driver.find_element_by_id("create-user").click()
        driver.find_element_by_id("tf_nom").send_keys(SCODOC_ENS_ID)
        driver.find_element_by_id("tf_user_name").send_keys(SCODOC_ENS_ID)
        driver.find_element_by_id("tf_prenom").send_keys(PRENOM_ENS)
        driver.find_element_by_id("tf_passwd").send_keys(SCODOC_ENS_PASS)
        driver.find_element_by_id("tf_passwd2").send_keys(SCODOC_ENS_PASS)
        driver.find_element_by_xpath("//input[@value='" + constructValue + "']").click()
        driver.find_element_by_xpath("//input[@name='force:list']").click()
        driver.find_element_by_id("tf_submit").click()
        driver.find_element_by_id("link-view-users").click()
    driver.close()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="05_Saisie_note_tests",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
