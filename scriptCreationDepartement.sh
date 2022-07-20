#!/bin/bash
#Se script se charge de se connecter au serveur scodoc et créer le département donné en paramètre
if [ "$#" -ne 2 ];
then
    echo "Pas assez d'arguments"
    exit 2
fi
ssh $1 /bin/bash<< EOF
cd /opt/scodoc/Products/ScoDoc/config
./create_dept.sh -n ${2}
EOF