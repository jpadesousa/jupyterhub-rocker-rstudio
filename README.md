# jupyterhub-rocker-rstudio

<img src="assets/hublogo.png" alt="Jupyterhub logo" title="Jupyterhub logo" width="100" style="margin-right: 20px; vertical-align: top;"> <img src="assets/rocker.png" alt="ETH Zurich logo" title="ETH Zurich logo" width="50" style="margin-right: 20px; vertical-align: top;"> <img src="assets/eth_logo.png" alt="ETH Zurich logo" title="ETH Zurich logo" width="150" style="vertical-align: top;">

## Description

This repository offers a deployment solution for [JupyterHub](https://jupyter.org/hub) on a server used by a small team, leveraging Docker to spawn images from [The Rocker Project](https://rocker-project.org/). The primary objective is to facilitate the management of multiple concurrent R versions, enabling users to select the appropriate version for their projects. Furthermore, Rocker Docker images apply a timestamp to R package installations, ensuring consistency by aligning package versions with the Docker image version.

## Quick demo

![Demo Animation](assets/demo.gif "Demo")

## Features

- Simplified deployment of [JupyterHub](https://jupyter.org/hub) within a Docker container.
- Isolation of running user notebooks from the hub through a separate [configurable-http-proxy](https://github.com/jupyterhub/configurable-http-proxy).
- Option to incorporate [nginx](https://nginx.org/en/) as a reverse proxy for improved performance and security.
- Integration with [DockerSpawner](https://github.com/jupyterhub/dockerspawner) allows for the spawning of multiple notebook or RStudio containers for both individual and multiple users simultaneously.
- Implementation of [LDAP authentication](https://github.com/jupyterhub/ldapauthenticator) for secure user verification.
- Compatibility with [The Rocker Project](https://rocker-project.org/) Docker images and [JupyterHub Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/) notebooks.
- Ensures data persistence through the use of a SQLite database, complemented by secure backups with [restic](https://restic.net/).

## Installation Guide

Follow these steps to set up the environment:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jpadesousa/jupyterhub-rocker-rstudio.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd jupyterhub-rocker-rstudio
   ```

3. **Create Environment Variables File**

   Create a `.envs` directory and then a `.env` file within it for storing your environment variables:

   ```bash
   mkdir .envs && touch .envs/.env
   ```

4. **Configure Environment Variables**

   Edit the `.envs/.env`, `docker-compose.yml`, and `docker-compose.rstudio.yml` files according to the guide provided in the [Configuring Environmental Variables](#configuring-environmental-variables) section below to customize the environment variables for your setup.

5. **Build Docker Services**

   Build the Docker services, volumes, and network using the following command:

   ```bash
   docker compose -f docker-compose.yml build
   ```

   To include the extended [josousa/rocker_rstudio_extended](https://hub.docker.com/repository/docker/josousa/rocker_rstudio_extended) images, use:

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.rstudio.yml build
   ```

6. **Run Docker Services**

   ```bash
   docker-compose up -d configurable_http_proxy jupyterhub restic_backup
   ```

## Configuring Environmental Variables

Customizing the environmental variables is a crucial step to tailor the project to your specific system requirements. You will need to modify two key files: `docker-compose.yml` and `.envs/.env`.

### docker-compose.yml

---

#### configurable_http_proxy

When setting up `configurable_http_proxy`, it's important to adjust the IP addresses and ports based on whether you're implementing SSL or utilizing a reverse proxy. For comprehensive guidance, refer to the [configurable-http-proxy documentation](https://github.com/jupyterhub/configurable-http-proxy).

Below is an example configuration for `configurable_http_proxy` within a Dockerfile:

```yml
command: >
  configurable-http-proxy
  --port=8000
  --api-ip=0.0.0.0
  --api-port=8001
  --default-target=http://jupyterhub:8081
  --error-target=http://jupyterhub:8081/hub/error
```

Ensure you adjust the port mappings to fit your setup. In this example, mapping port 8787 on the host to port 8000 on the container makes JupyterHub accessible at http://localhost:8787:

```yml
ports:
  - "8787:8000"
```

#### jupyterhub

In this section, you can define the JupyterHub version and, crucially, the Docker group ID (`GID`) from your host machine. This setup allows the JupyterHub Docker service to operate under the non-root `jupyterhub` user for enhanced security. By specifying the Docker `GID`, the `jupyterhub` user within the Docker container gains the ability to spawn additional Docker containers on the host machine. For detailed guidance on managing Docker as a non-root user, visit [Docker's official documentation](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

Additionally, if your server requires internet access through a proxy, you can specify an HTTP proxy.

Below is an example configuration in the `docker-compose.yml` file:

```yml
build:
  context: .
  dockerfile: ./compose/jupyterhub/Dockerfile
  args:
    - JUPYTERHUB_VERSION=5.0.0
    - DOCKER_GID=981 # Default: 1000
    - HTTP_PROXY=http://proxy.ethz.ch:3128
image: jupyterhub:5.0.0
```

#### nginx - reverse proxy (optional)

This section guides you through setting up [nginx](https://nginx.org/en/) as a reverse proxy, which is optional and may not be necessary if you're deploying the project within a private network.

To configure nginx, you'll need to specify several parameters in the Dockerfile, including the version of the nginx Docker image, the incoming port, and the domain name where your JupyterHub application will be accessible. Additionally, you'll configure SSL by specifying paths to your SSL certificate (`FULLCHAIN`), private key (`PRIVKEY`), and Diffie-Hellman parameters (`DHPARAM`). The `CERTS_DIR` variable indicates the directory inside the container where these certificates will be stored. Ensure you also mount the corresponding certificates folder from your host machine to the `CERTS_DIR` directory inside the container using the volume mount syntax: `./certs:/etc/nginx/ssl:ro`.

For detailed implementation insights and to make any necessary modifications, please refer to the `./compose/nginx/Dockerfile` and `./config/nginx/default.conf` files.

Below is an example configuration for nginx in your `docker-compose.yml` file:

```yml
nginx:
  build:
    context: .
    dockerfile: ./compose/nginx/Dockerfile
    args:
      - IMAGE_TAG=stable-alpine
      - INCOMING_PORT=443
      - DOMAIN=domain.example.com
      - FULLCHAIN=fullchain.pem
      - PRIVKEY=privkey.pem
      - DHPARAM=ssl-dhparams.pem
      - CERTS_DIR=/etc/nginx/ssl
  image: nginx:stable-alpine
  container_name: nginx
  volumes:
    - ./certs:/etc/nginx/ssl:ro
  ports:
    - "443:443"
  depends_on:
    - jupyterhub
  networks:
    - jupyterhub_network
```

#### volumes

This section outlines how to configure persistent storage for user data and backups, ensuring data persistence across all users. For instance, the SQLite database is stored at `/scratch/.sessions/jupyterhub`, and backups are stored at `/scratch/.backups/jupyterhub`. These locations are on the host machine and are mounted into each spawned container for access. This setup is achieved using a [`pre_spawn_hook`](https://jupyterhub.readthedocs.io/en/stable/reference/api/spawner.html), which is detailed in the file `./config/jupyterhub/pre_spawn_hook.py`. You can customize this file to control volume mounting in spawned notebook servers for individual users.

Below is an example configuration for defining volumes in your `docker-compose.yml` file:

```yml
volumes:
  session_data:
    driver: local
    driver_opts:
      type: none
      device: /scratch/.sessions/jupyterhub
      o: bind
  session_data_backup:
    driver: local
    driver_opts:
      type: none
      device: /scratch/.backups/jupyterhub
      o: bind
```

The `pre_spawn_hook` function is used to conditionally mount additional volumes based on environment variables. Here's how it's implemented:

```python
from distutils.util import strtobool
import os

def pre_spawn_hook(spawner):
    # Check if the scratch folder should be mounted
    mount_scratch = os.getenv("PRE_SPAWN_HOOK_MOUNT_SCRATCH", "false")
    if strtobool(mount_scratch):
        scratch_folder_on_host = "/scratch"
        container_scratch_path = "/scratch"
        spawner.volumes[scratch_folder_on_host] = container_scratch_path

    # Check if the user's public folder should be mounted
    mount_public = os.getenv("PRE_SPAWN_HOOK_MOUNT_PUBLIC", "false")
    if strtobool(mount_public):
        username = spawner.user.name
        user_public_folder_on_host = f"/home/{username}/public"
        container_public_path = "/public"
        spawner.volumes[user_public_folder_on_host] = container_public_path
```

### .envs/.env

---

#### Mandatory Variables

- **RESTIC_PASSWORD**: Specify the password for [restic](https://restic.net/) backups.
- **JUPYTERHUB_CRYPT_KEY**: Essential for encryption, details at [JupyterHub's Authenticators](https://jupyterhub.readthedocs.io/en/latest/reference/authenticators.html).
- **CONFIGPROXY_AUTH_TOKEN**: Required for the proxy, see [Separating Proxy](https://jupyterhub.readthedocs.io/en/latest/howto/separate-proxy.html).

#### Optional Variables - JupyterHub

Define JupyterHub configuration variables as needed. For more details, see `./config/jupyterhub/jupyterhub_config.py`.

#### Optional Variables - LDAPAuthenticator

For LDAPAuthenticator users, fill in your LDAP server variables. More info at [LDAPAuthenticator GitHub](https://github.com/jupyterhub/ldapauthenticator). ETH Zürich colleagues can contact me for LDAP configuration assistance.

#### Optional Variables - Docker Spawner Options

Authenticated users can select the Docker container to spawn. Available images are defined by `DOCKER_NOTEBOOKS = "rstudio:4.4.0,rstudio:4.3.3,rstudio:4.2.2,jupyter/datascience-notebook:2023-10-20"`. Docker will check for these images locally before attempting to download them from DockerHub.

#### Optional Variables - Docker Notebook UID and GID

- **DOCKER_NOTEBOOK_USERID**
- **DOCKER_NOTEBOOK_GROUPID**

These set the USERID and GROUPID (for RStudio) and NB_UID and NB_GID (for Jupyter notebooks) environment variables, aligning user IDs across the system. By default, it uses LDAP user information but falls back to default values if not specified.

#### Optional Variables - DockerSpawner

Configure CPU and memory allocation for Docker notebook containers:

- **DOCKERSPAWNER_CPU_GUARANTEE** and **DOCKERSPAWNER_CPU_LIMIT** for CPU resources.
- **DOCKERSPAWNER_MEM_GUARANTEE** and **DOCKERSPAWNER_MEM_LIMIT** for memory resources.
  Refer to the [DockerSpawner API](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html) for more details.

#### Optional Variables - Pre-Spawn Hook

Enables mounting `/scratch` and `/home/{username}/public` at container startup, facilitating file access. Adjust `./config/jupyterhub/pre_spawn_hook.py` as needed for your setup.

#### `.envs/.env`:

```bash
# MANDATORY
# ----------------------------
RESTIC_PASSWORD="example_password"
JUPYTERHUB_CRYPT_KEY="example_crypt_key"
CONFIGPROXY_AUTH_TOKEN="example_token"

# OPTIONAL - Jupyterhub configuration
# ----------------------------
JUPYTERHUB_ADMIN_USERS = "josousa" # Default: ""
JUPYTERHUB_DEFAULT_URL = "/hub/spawn" # Default: "/hub/spawn"
JUPYTERHUB_ANY_ALLOW_CONFIG = True # Default: False
JUPYTERHUB_ALLOW_ALL = True # Default: False
JUPYTERHUB_BIND_URL = "http://:8000" # Default: "http://:8000"
JUPYTERHUB_ACTIVE_SERVER_LIMIT = 0 # Default: 0 (unlimited)
JUPYTERHUB_AUTHENTICATOR_CLASS = "ldapauthenticator.LDAPAuthenticator" # Default: "jupyterhub.auth.PAMAuthenticator"

# LDAPAuthenticator configuration (no defaults)
# ----------------------------
LDAP_AUTHENTICATOR_SERVER_ADDRESS = ''
LDAP_AUTHENTICATOR_SERVER_PORT = 636
LDAP_AUTHENTICATOR_USE_SSL = True
LDAP_AUTHENTICATOR_LOOKUP_DN = True
LDAP_AUTHENTICATOR_LOOKUP_DN_SEARCH_FILTER = ''
LDAP_AUTHENTICATOR_LOOKUP_DN_SEARCH_USER = ''
LDAP_AUTHENTICATOR_LOOKUP_DN_SEARCH_PASSWORD = ''
LDAP_AUTHENTICATOR_USER_SEARCH_BASE = ''
LDAP_AUTHENTICATOR_USER_ATTRIBUTE = ''
LDAP_AUTHENTICATOR_LOOKUP_DN_USER_DN_ATTRIBUTE = ''
LDAP_AUTHENTICATOR_AUTH_STATE_ATTRIBUTES = 'uidNumber,gidNumber'
# Priorizes uidNumber and gidNumber to assign UserID and GroupID. If those are not available, it tries to use agrlUidNumber and agrlGidNumber.

# OPTIONAL - Options form spawner
# ----------------------------
# List of Docker notebooks
# Default: jupyter/minimal-notebook:latest
DOCKER_NOTEBOOKS = "rstudio:4.4.0,rstudio:4.3.3,rstudio:4.2.2,jupyter/datascience-notebook:2023-10-20"

# Ports for each notebook
# Default: 8888
DOCKER_NOTEBOOK_PORTS = '{ "rstudio": 8888, "jupyter/datascience-notebook": 8888 }'

# Directories for each notebook
# Default: /home/jovyan/work
DOCKER_NOTEBOOK_DIR = '{ "rstudio": "/home/rstudio", "jupyter/datascience-notebook": "/home/jovyan/work" }'

# Default URL for each notebook
# Default: /lab
DOCKER_NOTEBOOK_DEFAULT_URL = '{ "rstudio": "/rstudio", "jupyter/datascience-notebook": "/lab" }'

# Volumes to add to each notebook
# The volume jupyterhub-user-{username} is already mapped to DOCKER_NOTEBOOK_DIR
# Default: '{}'
# DOCKER_NOTEBOOK_ADD_VOLUMES = '{ "jupyterhub_scratch_data": "/scratch/data" }'

# OPTIONAL - DOCKER NOTEBOOK USER ID and GROUP ID
# ----------------------------
# Set USERID and NB_UID enviromental variables
# DOCKER_NOTEBOOK_USERID = 1000 # If not set, it fetches from LDAP. If LDAP is not set, it defaults to 1000

# Set GROUPID and NB_GID enviromental variables
# DOCKER_NOTEBOOK_GROUPID = 1000 # If not set, it fetches from LDAP. If LDAP is not set, it defaults to 1000

# OPTIONAL - DockerSpawner configuration
# ----------------------------
DOCKERSPAWNER_CPU_GUARANTEE = 1 # Default: No limit
DOCKERSPAWNER_CPU_LIMIT = 63 # Default: No limit
DOCKERSPAWNER_MEM_GUARANTEE = '5G' # Default: No limit
DOCKERSPAWNER_MEM_LIMIT = '85G' # Default: No limit

# OPTIONAL - Pre spawn hook
# ----------------------------
# Mount /scratch to /scratch
PRE_SPAWN_HOOK_MOUNT_SCRATCH = False # Default: False

# Mount /home/{username}/public to /public
PRE_SPAWN_HOOK_MOUNT_PUBLIC = False # Default: False

```

## Acknowledgements

This project draws inspiration from various GitHub repositories, tutorials, reference guides, and forum discussions. It also depends on numerous open-source software projects. I extend my gratitude to all developers for their invaluable guidance and support to the community. The contributions of [Ryan Lovett](https://github.com/ryanlovett) and [Yuvi Panda](https://github.com/yuvipanda) were particularly noteworthy.

Key resources include:

- [jupyter-rsession-proxy](https://github.com/jupyterhub/jupyter-rsession-proxy)
- [jupyterhub-ldapauthenticator](https://github.com/jupyterhub/ldapauthenticator)
- [dockerspawner](https://github.com/jupyterhub/dockerspawner)
- [The Rocker Project](https://rocker-project.org/)
- [JupyterHub](https://jupyter.org/hub)
- [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/)

## Contributing

Your contributions are welcome! Whether you have ideas, suggestions, or bug reports, feel free to open an issue or submit a pull request. This project was initially designed to address a specific challenge within our team but can be adapted to suit other computational environments with some modifications.

## Contact

Should you have any questions or wish to get in touch, please contact me at [joao.agostinhodesousa@hest.ethz.ch](mailto:joao.agostinhodesousa@hest.ethz.ch).
