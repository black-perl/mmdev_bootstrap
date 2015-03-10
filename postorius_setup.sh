#!/bin/bash
cd $VE_POSTORIUS
source bin/activate
cd $POSTORIUS_DIR 
cd postorius/
python setup.py develop
cd ../mailman.client
python setup.py develop
cd ../postorius_standalone
python manage.py runserver
deactivate

