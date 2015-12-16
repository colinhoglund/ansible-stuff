#!/bin/bash

ec2_inv=$(dirname $0)/ec2.py

# pull down newest ec2.py inventory script
wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.py -O $ec2_inv
chmod +x $ec2_inv
