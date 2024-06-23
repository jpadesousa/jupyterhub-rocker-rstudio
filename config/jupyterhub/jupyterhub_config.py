import os
from distutils.util import strtobool
from options_form_spawner import OptionsFormSpawner
from auth_state_hook import auth_state_hook
from pre_spawn_hook import pre_spawn_hook

c = get_config()  # noqa

# JupyterHub configuration
c.JupyterHub.spawner_class = OptionsFormSpawner
c.JupyterHub.allow_named_servers = True
c.JupyterHub.active_server_limit = int(os.getenv("JUPYTERHUB_ACTIVE_SERVER_LIMIT", 0))
c.JupyterHub.default_url = os.getenv("JUPYTERHUB_DEFAULT_URL", "/hub/spawn")
c.JupyterHub.log_level = "DEBUG"
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.bind_url = os.getenv("JUPYTERHUB_BIND_URL", "http://:8000")
c.JupyterHub.db_url = "sqlite:///data/jupyterhub.sqlite"

# Authenticator configuration
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
c.Authenticator.enable_auth_state = True

# If the authenticator is set to use LDAP, configure the LDAP settings
if os.getenv("JUPYTERHUB_AUTHENTICATOR_CLASS") == "ldapauthenticator.LDAPAuthenticator":
    c.LDAPAuthenticator.server_address = os.getenv("LDAP_AUTHENTICATOR_SERVER_ADDRESS")
    c.LDAPAuthenticator.server_port = int(os.getenv("LDAP_AUTHENTICATOR_SERVER_PORT"))
    c.LDAPAuthenticator.use_ssl = bool(
        strtobool(os.getenv("LDAP_AUTHENTICATOR_USE_SSL"))
    )
    c.LDAPAuthenticator.lookup_dn = bool(
        strtobool(os.getenv("LDAP_AUTHENTICATOR_LOOKUP_DN"))
    )
    c.LDAPAuthenticator.lookup_dn_search_filter = os.getenv(
        "LDAP_AUTHENTICATOR_LOOKUP_DN_SEARCH_FILTER"
    )
    c.LDAPAuthenticator.lookup_dn_search_user = os.getenv(
        "LDAP_AUTHENTICATOR_LOOKUP_DN_SEARCH_USER"
    )
    c.LDAPAuthenticator.lookup_dn_search_password = os.getenv(
        "LDAP_AUTHENTICATOR_LOOKUP_DN_SEARCH_PASSWORD"
    )
    c.LDAPAuthenticator.user_search_base = os.getenv(
        "LDAP_AUTHENTICATOR_USER_SEARCH_BASE"
    )
    c.LDAPAuthenticator.user_attribute = os.getenv("LDAP_AUTHENTICATOR_USER_ATTRIBUTE")
    c.LDAPAuthenticator.lookup_dn_user_dn_attribute = os.getenv(
        "LDAP_AUTHENTICATOR_LOOKUP_DN_USER_DN_ATTRIBUTE"
    )
    c.LDAPAuthenticator.auth_state_attributes = os.getenv(
        "LDAP_AUTHENTICATOR_AUTH_STATE_ATTRIBUTES"
    ).split(",")

# Spawner configuration
c.Spawner.environment = {"TERM": "xterm-color"}
if os.getenv("JUPYTERHUB_AUTHENTICATOR_CLASS") == "ldapauthenticator.LDAPAuthenticator":
    c.Spawner.auth_state_hook = auth_state_hook
else:
    userid = str(os.getenv("DOCKER_NOTEBOOK_USERID", 1000))
    groupid = str(os.getenv("DOCKER_NOTEBOOK_GROUPID", 1000))
    c.Spawner.environment.update(
        {"USERID": userid, "GROUPID": groupid, "NB_UID": userid, "NB_GID": groupid}
    )

c.Spawner.pre_spawn_hook = pre_spawn_hook
c.DockerSpawner.remove = True  # Remove containers after they stop
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = "jupyterhub_network"
c.DockerSpawner.http_timeout = int(900)
c.DockerSpawner.start_timeout = int(900)
if os.getenv("DOCKERSPAWNER_CPU_GUARANTEE") is not None:
    c.DockerSpawner.cpu_guarantee = int(os.getenv("DOCKERSPAWNER_CPU_GUARANTEE"))

if os.getenv("DOCKERSPAWNER_CPU_LIMIT") is not None:
    c.DockerSpawner.cpu_limit = int(os.getenv("DOCKERSPAWNER_CPU_LIMIT"))

if os.getenv("DOCKERSPAWNER_MEM_GUARANTEE") is not None:
    c.DockerSpawner.mem_guarantee = os.getenv("DOCKERSPAWNER_MEM_GUARANTEE")

if os.getenv("DOCKERSPAWNER_MEM_LIMIT") is not None:
    c.DockerSpawner.mem_limit = os.getenv("DOCKERSPAWNER_MEM_LIMIT")
