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

urlMatiere = ""
listeEtudiant = []
global MOY_UE1
global MOY_UE2
global URL_SEMESTRE
global COEFFUE1
global COEFFUE2


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

    # Test: Ajout de note pour deux élèves dans une seule UE et vérifie si la moyenne de cet UE sur la fiche étudiante correspondant à la valeur rentrée
    # @expected : La note rentrée et la moyenne sont identiques
    def test_010_ajout_note_multiple_pour_une_ue(self):
        global listeEtudiant
        global MOY_UE1
        global URL_SEMESTRE
        driver = self.driver
        url = self.url
        driver.get(url)
        linkAddNote = "formnotes_note_"
        driver.find_element_by_link_text("semestre 1").click()
        self.wait.until(EC.url_changes(url))
        URL_SEMESTRE = driver.current_url
        ue_name = driver.find_elements_by_class_name("status_ue_acro")[0].text
        driver.find_element_by_link_text("M1101").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        driver.find_element_by_xpath("//a[contains(@href,'saisie_notes?')]").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        URL = driver.current_url
        for champs in driver.find_elements_by_xpath(
            "//input[contains(@id,'" + linkAddNote + "')]"
        ):
            champs.clear()
            champs.send_keys(12)
            idChamp = champs.get_attribute("id")
            idEtud = idChamp[len(linkAddNote) : len(idChamp)]
            if idEtud not in listeEtudiant:
                listeEtudiant.append(idEtud)
        driver.find_element_by_id("formnotes_submit").click()
        self.wait.until(EC.url_changes(URL))
        driver.get(URL_SEMESTRE)
        noteBonne = True
        # print(listeEtudiant)
        for etudiant in listeEtudiant:
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            time.sleep(5)
            MOY_UE1 = driver.find_element_by_id("ue-" + ue_name.lower().replace(" ","-")).text
            if "12" not in MOY_UE1:
                noteBonne = False
        self.assertTrue(noteBonne)

    # Test : Ajoute une note à la seconde UE pour les deux élèves
    # @expected : La moyenne de la seconde UE apparait et corresponds à la note rentrée
    def test_020_ajout_note_seconde_ue(self):
        global listeEtudiant
        global MOY_UE2
        global URL_SEMESTRE
        linkAddNote = "formnotes_note_"
        driver = self.driver
        url = self.url
        driver.get(URL_SEMESTRE)
        ue_name = driver.find_elements_by_class_name("status_ue_acro")[1].text
        driver.find_element_by_link_text("M1201").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        driver.find_element_by_xpath("//a[contains(@href,'saisie_notes?')]").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        URL = driver.current_url
        for champs in driver.find_elements_by_xpath(
            "//input[contains(@id,'" + linkAddNote + "')]"
        ):
            champs.clear()
            champs.send_keys(8)
        driver.find_element_by_id("formnotes_submit").click()
        self.wait.until(EC.url_changes(URL))
        driver.get(URL_SEMESTRE)
        noteBonne = True
        for etudiant in listeEtudiant:
            URL = driver.current_url
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            time.sleep(5)
            MOY_UE2 = driver.find_element_by_id("ue-" + ue_name.lower().replace(" ","-")).text
            if "8" not in MOY_UE2:
                noteBonne = False

        self.assertTrue(noteBonne)

    # Test : Vérification calcul de la moyenne générale
    # @expected La moyenne prends en compte les deux ue et leur coefficiant
    def test_030_verification_moyenne_generale(self):
        global COEFF_UE1
        global COEFF_UE2
        COEFF_UE1 = 2
        COEFF_UE2 = 2
        driver = self.driver
        url = self.url
        driver.get(url)
        moyenneBonne = True
        for etudiant in listeEtudiant:
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            time.sleep(5)
            if (
                (float(MOY_UE1) * COEFF_UE1 + float(MOY_UE2) * COEFF_UE2)
                / (COEFF_UE1 + COEFF_UE2)
            ) != float(driver.find_element_by_class_name("rcp_moy").text):
                moyenneBonne = False
        self.assertTrue(moyenneBonne)

    # Test : Changement du coefficiant d'un module et de ce fait, du coefficiant de l'UE
    # @expected : La moyenne générale se modifie en fonction de ce changement de coefficiant
    def test_040_modification_coefficiant_module(self):
        global COEFF_UE1
        COEFF_UE1 = 3
        driver = self.driver
        url = self.url
        driver.get(url)
        driver.find_element_by_id("link-programmes").click()
        driver.find_element_by_id("titre-dut-info").click()
        driver.find_element_by_xpath("//span[contains(text(),'M1101')]").click()
        driver.find_element_by_id("tf_coefficient").clear()
        driver.find_element_by_id("tf_coefficient").send_keys(COEFF_UE1)
        URL = driver.current_url
        driver.find_element_by_id("tf_submit").click()
        self.wait.until(EC.url_changes(URL))
        moyenneBonne = True
        for etudiant in listeEtudiant:
            URL = driver.current_url
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            time.sleep(5)
            if (
                (float(MOY_UE1) * COEFF_UE1 + float(MOY_UE2) * COEFF_UE2)
                / (COEFF_UE1 + COEFF_UE2)
            ) != float(driver.find_element_by_class_name("rcp_moy").text):
                moyenneBonne = False
            self.assertTrue(moyenneBonne)

    # Test : Ajout d'une note bonus pour un étudiant et d'une note malus pour un autre
    # @expected : La moyenne de l'UE où est ajouté la note bonus/malus est impactée par cette dernière, la moyenne générale change avec ce changement de moyenne d'UE
    def test_050_ajout_note_bonus(self):
        moyenneBonusEtudiant1 = "0.25"
        moyenneBonusEtudiant2 = "0.25"
        linkAddNote = "formnotes_note_"
        driver = self.driver
        driver.get(URL_SEMESTRE)
        driver.find_element_by_partial_link_text("malus").click()
        driver.find_element_by_link_text("Créer nouvelle évaluation").click()
        time.sleep(1)
        driver.find_element_by_name("jour").clear()
        driver.find_element_by_name("jour").send_keys("31/01/2021")
        driver.find_element_by_id("tf_description").send_keys("une interrogation bonus")
        driver.find_element_by_id("tf_submit").click()
        time.sleep(1)
        driver.find_element_by_xpath("//a[contains(@href,'saisie_notes?')]").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        champsNote = driver.find_elements_by_xpath(
            "//input[contains(@id,'" + linkAddNote + "')]"
        )
        champsNote[0].clear()
        champsNote[1].clear()
        champsNote[0].send_keys("-" + moyenneBonusEtudiant1)
        champsNote[1].send_keys(moyenneBonusEtudiant2)
        driver.find_element_by_id("formnotes_submit").click()
        numeroEtu = 0
        moyenneBonne = True
        for etudiant in listeEtudiant:
            URL = driver.current_url
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            time.sleep(5)
            if numeroEtu == 0:
                if (
                    (
                        float(MOY_UE1) * COEFF_UE1
                        + (float(MOY_UE2) + float(moyenneBonusEtudiant1)) * COEFF_UE2
                    )
                    / (COEFF_UE1 + COEFF_UE2)
                ) != float(driver.find_element_by_class_name("rcp_moy").text):
                    moyenneBonne = False
            elif numeroEtu == 1:
                if (
                    (
                        float(MOY_UE1) * COEFF_UE1
                        + (float(MOY_UE2) - float(moyenneBonusEtudiant2)) * COEFF_UE2
                    )
                    / (COEFF_UE1 + COEFF_UE2)
                ) != float(driver.find_element_by_class_name("rcp_moy").text):
                    moyenneBonne = False
            numeroEtu = numeroEtu + 1
        self.assertTrue(moyenneBonne)

    # Test : Ajout d'une note en attente pour un étudiant, et d'une note entrée pour un autre sur une même évaluation
    # @expected :
    def test_060_note_attente(self):
        moyenneBonusEtudiant1 = "0.25"
        moyenneBonusEtudiant2 = "0.25"
        linkAddNote = "formnotes_note_"
        champsNote = []
        driver = self.driver
        driver.get(URL_SEMESTRE)
        driver.find_element_by_link_text("M1101").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        driver.find_element_by_xpath("//a[contains(@href,'saisie_notes?')]").click()
        URL = driver.current_url
        champsNote = driver.find_elements_by_xpath(
            "//input[contains(@id,'" + linkAddNote + "')]"
        )
        champsNote[0].clear()
        champsNote[0].send_keys("ATT")
        driver.find_element_by_id("formnotes_submit").click()
        self.wait.until(EC.url_changes(URL))
        numeroEtu = 0
        moyenneBonne = True
        affichageMoyenne = True
        for etudiant in listeEtudiant:
            URL = driver.current_url
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            time.sleep(5)
            ueListElement = driver.find_elements_by_class_name("ue_acro")
            ueListText = []
            for ueElement in ueListElement:
                ueListText.append(ueElement.text)
            if numeroEtu == 0:
                moyEtudiant1 = float(MOY_UE2) + float(moyenneBonusEtudiant1)
                if moyEtudiant1 != float(
                    driver.find_element_by_class_name("rcp_moy").text
                ):
                    moyenneBonne = False
                if "UE11" in ueListText:
                    affichageMoyenne = False
            elif numeroEtu == 1:
                moyEtudiant2 = (
                    float(MOY_UE1) * COEFF_UE1
                    + (float(MOY_UE2) - float(moyenneBonusEtudiant2)) * COEFF_UE2
                ) / (COEFF_UE1 + COEFF_UE2)
                if moyEtudiant2 != float(
                    driver.find_element_by_class_name("rcp_moy").text
                ):
                    moyenneBonne = False
                if "UE11" not in ueListText:
                    affichageMoyenne = False
            numeroEtu = numeroEtu + 1
        self.assertTrue(moyenneBonne and affichageMoyenne)

    def test_070_note_absent(self):
        ue_name = "UE11"
        moyenneBonusEtudiant1 = "0.25"
        moyenneBonusEtudiant2 = "0.25"
        linkAddNote = "formnotes_note_"
        MOY_UE1_EXC = 0
        champsNote = []
        driver = self.driver
        driver.get(URL_SEMESTRE)
        driver.find_element_by_link_text("M1101").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        driver.find_element_by_xpath("//a[contains(@href,'saisie_notes?')]").click()
        URL = driver.current_url
        champsNote = driver.find_elements_by_xpath(
            "//input[contains(@id,'" + linkAddNote + "')]"
        )
        champsNote[0].clear()
        champsNote[0].send_keys("ABS")
        driver.find_element_by_id("formnotes_submit").click()
        self.wait.until(EC.url_changes(URL))
        numeroEtu = 0
        moyenneBonne = True
        affichageMoyenne = True
        noteExcuseeEgaleAZero = True
        ueList = []
        for etudiant in listeEtudiant:
            URL = driver.current_url
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            self.wait.until(EC.url_changes(URL))
            ueListElement = driver.find_elements_by_class_name("ue_acro")
            ueListText = []
            for ueElement in ueListElement:
                ueListText.append(ueElement.text)
            if numeroEtu == 0:
                moyEtudiant1 = (
                    float(MOY_UE1_EXC) * COEFF_UE1
                    + ((float(MOY_UE2) + float(moyenneBonusEtudiant1)) * COEFF_UE2)
                ) / (COEFF_UE1 + COEFF_UE2)
                # print(format(moyEtudiant1, "2.2f"))
                # print(
                #    format(
                #        float(driver.find_element_by_class_name("rcp_moy").text), "2.2f"
                #    )
                # )
                if format(moyEtudiant1, "2.2f") != format(
                    float(driver.find_element_by_class_name("rcp_moy").text), "2.2f"
                ):
                    moyenneBonne = False
                if ue_name not in ueListText:
                    affichageMoyenne = False
                MOY_UE1 = driver.find_element_by_id("ue-" + ue_name.lower().replace(" ","-")).text
                if float(0) != float(MOY_UE1):
                    noteExcuseeEgaleAZero = False
            elif numeroEtu == 1:
                MOY_UE1 = driver.find_element_by_id("ue-" + ue_name.lower().replace(" ","-")).text
                moyEtudiant2 = (
                    float(MOY_UE1) * COEFF_UE1
                    + (float(MOY_UE2) - float(moyenneBonusEtudiant2)) * COEFF_UE2
                ) / (COEFF_UE1 + COEFF_UE2)
                if moyEtudiant2 != float(
                    driver.find_element_by_class_name("rcp_moy").text
                ):
                    moyenneBonne = False
                if "UE11" not in ueListText:
                    affichageMoyenne = False
            numeroEtu = numeroEtu + 1
        self.assertTrue(moyenneBonne and affichageMoyenne and noteExcuseeEgaleAZero)

    def test_080_note_excuse(self):
        moyenneBonusEtudiant1 = "0.25"
        moyenneBonusEtudiant2 = "0.25"
        linkAddNote = "formnotes_note_"
        champsNote = []
        driver = self.driver
        driver.get(URL_SEMESTRE)
        driver.find_element_by_link_text("M1101").click()
        self.wait.until(EC.url_changes(URL_SEMESTRE))
        driver.find_element_by_xpath("//a[contains(@href,'saisie_notes?')]").click()
        URL = driver.current_url
        champsNote = driver.find_elements_by_xpath(
            "//input[contains(@id,'" + linkAddNote + "')]"
        )
        champsNote[0].clear()
        champsNote[0].send_keys("EXC")
        driver.find_element_by_id("formnotes_submit").click()
        self.wait.until(EC.url_changes(URL))
        numeroEtu = 0
        moyenneBonne = True
        affichageMoyenne = True
        ueList = []
        for etudiant in listeEtudiant:
            URL = driver.current_url
            searchBar = driver.find_element_by_id("in-expnom")
            searchBar.send_keys(etudiant)
            searchBar.submit()
            self.wait.until(EC.url_changes(URL))
            ueListElement = driver.find_elements_by_class_name("ue_acro")
            ueListText = []
            for ueElement in ueListElement:
                ueListText.append(ueElement.text)
            if numeroEtu == 0:
                moyEtudiant1 = float(MOY_UE2) + float(moyenneBonusEtudiant1)
                if moyEtudiant1 != float(
                    driver.find_element_by_class_name("rcp_moy").text
                ):
                    moyenneBonne = False
                if "UE11" in ueListText:
                    affichageMoyenne = False
            elif numeroEtu == 1:
                moyEtudiant2 = (
                    float(MOY_UE1) * COEFF_UE1
                    + (float(MOY_UE2) - float(moyenneBonusEtudiant2)) * COEFF_UE2
                ) / (COEFF_UE1 + COEFF_UE2)
                if moyEtudiant2 != float(
                    driver.find_element_by_class_name("rcp_moy").text
                ):
                    moyenneBonne = False
                if "UE11" not in ueListText:
                    affichageMoyenne = False
            numeroEtu = numeroEtu + 1
        self.assertTrue(moyenneBonne and affichageMoyenne)

    # TOdo
    def test_090_note_bonus(self):
        global listeEtudiant
        global COEFF_UE1
        global COEFF_UE2
        global URL_SEMESTRE

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
        "test_scenario3_formation.py",
    ]
    process = subprocess.Popen(cmdProcess)
    process.wait()
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            report_name="06_Moyenne_tests",
            output="./ResultatTest",
            combine_reports=True,
        )
    )
