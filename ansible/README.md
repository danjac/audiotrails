Ansible playbooks for deploying [Radiofeed](https://github.com/danjac/radiofeed-app)

## Architecture

The architecture can run on cheap VM hosting e.g. Hetzner or Digital Ocean droplets. It assumes the following:

1. One server running PostgreSQL and Redis.
2. One server running cron jobs and managing Docker swarm.
3. Multiple app servers running a Gunicorn/Django instance (as Docker swarm workers).
4. Caching/CDN using Cloudflare.

The Ansible playbooks will deploy all of the above using Docker images.

## Setup

1. Copy the following files:

    * `hosts.yml.example` > `hosts.yml`
    * `vars/settings.yml.example` > `vars/settings.yml`

2. Edit the above files as required, adding your server-specific settings.
3. Encrypt the files using `ansible-vault` and make backups to a secure place.
4. In Cloudflare, create an [Origin Certificate](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/) and save the public and private keys to `roles/load_balancers/files/cloudflare.pem` and `roles/load_balancers/cloudflare.key` respectively. Remember to encrypt these files with ansible-vault.

## Deployment

For ease of use, a [justfile](https://github.com/casey/just) has been provided for running the Ansible playbooks.

You should have root SSH access to your servers.

1. Ensure you have access to a Radiofeed Docker image. The default image is `ghcr.io/danjac/radiofeed-app`.

2. Run `just deploy` to deploy to your servers.

## Upgrade

To update server dependencies, run `just pb upgrade`.

## Django management commands

Run `just pb dj_manage` to generate a `manage.sh` script in the local `ansible` directory. This will run Django management commands in the cron scheduler server:

```bash
just djmanage # run once to create the bash script

./manage.sh migrate --check
```
