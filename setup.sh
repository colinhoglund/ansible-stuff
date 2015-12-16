#!/bin/bash

# pull down newest ec2.py inventory script
wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.py -O $(dirname $0)/inventory/ec2.py
