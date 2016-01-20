#!/bin/bash

# pull down newest ec2.py inventory script and ec2.ini
ansible_dir=$(dirname $0)
ec2_py=${ansible_dir}/ec2.py
ec2_ini=${ansible_dir}/ec2.ini

wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.py -O $ec2_py
wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.ini -O $ec2_ini
chmod +x $ec2_py
