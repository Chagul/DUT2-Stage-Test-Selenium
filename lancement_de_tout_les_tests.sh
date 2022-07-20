#!/bin/bash
#Ce script lance en séquence les différents jeux de tests.
if [ "$#" -eq 1 ]
then
    if [ "$1" = "--cleanup" ] || [ "$1" = "--c" ]
    then
        rm -rf ./ResultatTest/*
    else
        echo "Mauvaise utilisation de la commande, utilisez --cleanup ou -c pour supprimer les anciens rapport de tests" 
    fi
fi
python3 01_creation_departement_test.py;
python3 02_creation_formation_test.py;
python3 03_etudiant_test.py;
python3 04_creation_absence_test.py;
python3 05_saisie_note_test.py;
python3 06_test_moyenne.py;
python3 07_test_admission.py;
python3 deleteDepartement.py;
./scriptGenerateReportPage.sh

