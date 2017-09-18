#!/bin/bash

dir="$(pwd)/db/sql/init.sql"
mysql -u $1 -e "CREATE DATABASE challenge_kyle"
mysql -u $1 challenge_kyle < $dir

pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
bower install
