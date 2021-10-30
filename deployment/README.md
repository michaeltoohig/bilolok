# Deployment Scripts

This directory contains Ansible playbooks for setting up production servers and deploying our application to those servers.

## Usage

To use these scripts yourself you will first need to install `ansible` to your local python environment. Personally, I prefer to keep deployment environment independent from the application environment.

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ansible
```

Then you can use the `ansible-playbook` command to run playbooks. But you will first want to modify the `environments/` files to match your needs.

```
ansible-playbook -K -i environments/production deploy-init.yml
```

## Notes

https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data-on-ubuntu-16-04
