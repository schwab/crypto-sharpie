#!/bin/bash

# setup slicer.ini with the correct database server ip
#cat slicer_localhost.ini | ./match_replace.py -m localhost -r $MDB_IP > slicer.ini
#echo 'replaced localhost with '$MDB_IP
# cat slicer_localhost.ini | ./match_replace.py -m localhost -r 172.17.0.2 > slicer.ini
# echo 'replaced localhost with '172.17.0.2

# Initialize the database schema if it's not already in place
#CONNECTION_STRING=$(cat slicer.ini | ./ini_value.py -s store -k url)
echo 'using connection string :'$CONNECTION_STRING
echo "notebook :"$JUPYTER_ENDPOINT

if [ "$JUPYTER_ENDPOINT" == "false" ]; then
    #./repo/anesthesia_models.py -d -i -c $CONNECTION_STRING
    echo "first command : "$1   
    if [ "$1" == "import" ]; then
        echo "Loading clean data"
        ./repo/coin_data_importer.py -c $CONNECTION_STRING 
    fi 
    echo 'starting slicer server using slicer.ini'
    slicer serve slicer.ini

else
    echo "starting jupyter notebook for mariadb"
    export JUPYTER_CONFIG_DIR=/srv/config
    jupyter notebook --allow-root --ip=0.0.0.0 --port=80
fi
