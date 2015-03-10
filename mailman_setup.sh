#!/bin/bash
cd $VE_MAILMAN
source bin/activate
cd $CORE_DIR
cd mailman
python setup.py develop
cd src/mailman
mailman start 
deactivate
