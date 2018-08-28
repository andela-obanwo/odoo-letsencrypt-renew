#!/bin/bash

# change directory to script location
cd ~/odoo-letsencrypt-renew

echo 'Script Started' >> logs/log.txt

# activate virtual environment
source odoo-letsencrypt-renew/bin/activate

# enable https access for certificate renewal
python manage_security_access.py enable_https

# attempt certificate renewal
source /etc/letsencrypt/renewal/renewalscript.sh >> logs/log.txt

# disable https access
python manage_security_access.py disable_https

echo 'Script Ended' >> logs/log.txt
