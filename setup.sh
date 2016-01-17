#!/bin/bash

# pull down newest ec2.py inventory script
ec2_inv=$(dirname $0)/ec2.py
wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.py -O $ec2_inv
chmod +x $ec2_inv
