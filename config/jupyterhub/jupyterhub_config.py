import os
from distutils.util import strtobool
from options_form_spawner import OptionsFormSpawner

c = get_config()  # noqa

# Set the custom spawner as the default spawner
c.JupyterHub.spawner_class = OptionsFormSpawner

# Enable named servers
c.JupyterHub.allow_named_servers = True

# Set the default URLs
c.JupyterHub.default_url = os.getenv("JUPYTERHUB_DEFAULT_URL", "/hub/spawn")

# Set the authenticator class and configure it
c.JupyterHub.authenticator_class = os.getenv(
    "JUPYTERHUB_AUTHENTICATOR_CLASS", "jupyterhub.auth.PAMAuthenticator"
)
admin_users = os.getenv("JUPYTERHUB_ADMIN_USERS", "")
c.Authenticator.admin_users = set(admin_users.split(",")) if admin_users else set()
c.Authenticator.any_allow_config = bool(
    strtobool(os.getenv("JUPYTERHUB_ANY_ALLOW_CONFIG", "False"))
)
c.Authenticator.allow_all = bool(strtobool(os.getenv("JUPYTERHUB_ALLOW_ALL", "False")))
c.Authenticator.delete_invalid_users = True

# If the authenticator is set to use LDAP, configure the LDAP settings
if os.getenv("JUPYTERHUB_AUTHENTICATOR_CLASS") == "ldapauthenticator.LDAPAuthenticator":
    c.LDAPAuthenticator.server_hosts = os.getenv("LDAP_AUTHENTICATOR_SERVER_HOSTS")
    c.LDAPAuthenticator.server_use_ssl = bool(
        strtobool(os.getenv("LDAP_AUTHENTICATOR_SERVER_USE_SSL"))
    )
    c.LDAPAuthenticator.server_port = int(os.getenv("LDAP_AUTHENTICATOR_SERVER_PORT"))
    c.LDAPAuthenticator.bind_user_dn = os.getenv("LDAP_AUTHENTICATOR_BIND_USER_DN")
    c.LDAPAuthenticator.bind_user_password = os.getenv(
        "LDAP_AUTHENTICATOR_BIND_USER_PASSWORD"
    )
    c.LDAPAuthenticator.user_search_base = os.getenv(
        "LDAP_AUTHENTICATOR_USER_SEARCH_BASE"
    )
    c.LDAPAuthenticator.user_search_filter = os.getenv(
        "LDAP_AUTHENTICATOR_USER_SEARCH_FILTER"
    )

# Configure the DockerSpawner to remove containers after they stop
c.DockerSpawner.remove = True

# Configure the Docker network
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = "jupyterhub_network"

# Set the log level and HTTP timeout
c.JupyterHub.log_level = "DEBUG"
c.DockerSpawner.http_timeout = int(900)
c.DockerSpawner.start_timeout = int(900)

# Configure the database for persistence
c.JupyterHub.db_url = "sqlite:///data/jupyterhub.sqlite"

# Set environment variables for the spawner
c.Spawner.environment = {"TERM": "xterm-color"}

# Set the IP address that the JupyterHub service will bind to
c.JupyterHub.hub_ip = "jupyterhub"

# Set the URL and port that the JupyterHub service will listen on
c.JupyterHub.bind_url = os.getenv("JUPYTERHUB_BIND_URL", "http://:8000")
