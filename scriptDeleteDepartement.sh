#!/bin/bash
#Se script se charge de se connecter au serveur scodoc et supprimer le département donné en paramètre
if [ "$#" -ne 2 ];
then
    echo "Pas assez d'arguments"
    exit 2
fi
ssh $1 /bin/bash<< EOF
cd /opt/scodoc/Products/ScoDoc/config
./delete_dept.sh -n ${2} 
EOF
ssh $1 'systemctl restart ScoDoc.service'