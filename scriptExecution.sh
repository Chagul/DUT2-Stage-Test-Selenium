#!/bin/bash
#Ce script se rends sur le serveur scodoc et lance le script précisé sur celui ci
if [ "$#" -ne 3 ];
then
    echo "Pas assez d'arguments"
    exit 2
fi
ssh $1 /bin/bash<< EOF
cd /opt/scodoc/Products/ScoDoc/
scotests/scointeractive.sh -r ${2} scotests/${3}
EOF
ssh $1 'systemctl restart ScoDoc.service'
