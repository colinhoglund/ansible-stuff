This role has been tested on ubuntu 14.04 and centos 7

Install python 2 and 3 with custom prefix and global packages
```
---

- hosts: all
  become: true
  vars:
    python_configure_prefix: /opt/local
    python_global_packages:
      - ansible==2.0.1.0
      - uwsgi
  roles:
    - { role: python, python_version: 2.7.7 }
    - { role: python, python_version: 3.4.4 }
```
