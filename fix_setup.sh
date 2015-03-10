#!/bin/bash

# set mailman
cd $VE_MAILMAN
source bin/activate
cd $DEVSETUP_DIR
cd mailman
python setup.py develop
deactivate

# set others
cd $VE_POSTORIUS
source bin/activate
cd $DEVSETUP_DIR 
cd postorius/
python setup.py develop
cd ../mailman.client
python setup.py develop
deactivate

