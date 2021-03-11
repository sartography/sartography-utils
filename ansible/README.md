#Ansible playbooks for server setups

digitalocean.yml contains a simple ansible playbook to set up a basic machine in Digital Ocean.

update the inventory with the correct IP and run it as follows:

`ansible-playbook -i hosts.dev ./digitalocean.yml -u root`
