This role has only been tested on ubuntu 14.04

Install python 2 and 3 with custom prefix and global packages
```
---
- hosts: localhost
  vars:
    python_configure_prefix: /opt/local
    python_global_packages:
      - uwsgi
  roles:
    - { role: python, python_version: 2.7.11 }
    - { role: python, python_version: 3.5.1 }
```
