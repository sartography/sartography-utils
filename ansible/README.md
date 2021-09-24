#Ansible playbooks for server setups

## Installing ansible on your machine

You can find the instructions here: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

These playbooks were tested on ansible 2.9.6


## Basic server setup

digitalocean.yml contains a simple ansible playbook to set up a basic ubuntu 20.04 machine in Digital Ocean.

First create your droplet with the appropriate ssh keys. You could also do this with any VM you set up yourself

Then update the inventory with the correct IP under `[digital_ocean]` and run it as follows:

`ansible-playbook -i hosts.dev ./digitalocean.yml -u root`

## Star Drive staging server setup

`star-drive.yml` contains an ansible playbook to set up a star drive staging server. Please run the `digitalocean.yml` playbook against your server *first*

Update the inventory with the correct IP under `[star-drive]` and run it as follows:

`ansible-playbook -i hosts.dev ./star-drive.yml`

Please note, this is a setup for staging purposes *ONLY*. It is not secure, API keys are not added, and while there is HTTP basic auth, there is no TLS (the password could be sniffed)

As there is and only should be testing data on these servers, it should be ok.

The database password is `ed_pass` by default, though it will prompt you for a password when you run the playbook. Should you wish to change this please update the configuration for flask in ./configs/star-drive/flask locally before running. If you specify another password on a subsequent run, it will be overwritten.

The basic auth password is `pQNww!iXo9EEi988&kr` by default, though it will prompt you for a password when you run the playbook. Should you wish to change this please make a note of it. If you specify another password on a subsequent run, it will be overwritten.


There are a few things that could have been done more efficiently - however I wanted to demonstrate the use of ( and not ) of variables etc, so that people can learn. 
