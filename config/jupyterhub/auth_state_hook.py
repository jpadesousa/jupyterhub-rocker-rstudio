import os


def auth_state_hook(spawner, auth_state):
    if not auth_state:
        spawner.log.info(f"No auth_state for user {spawner.user.name}")
        return

    # Get the uidNumber from the auth_state
    uid = os.getenv("DOCKER_NOTEBOOK_USERID")
    if not uid:
        uid = auth_state.get("uidNumber", [1000])[0]
        # Default to 1000 if uidNumber is not in auth_state

    # Get the gidNumber from the auth_state
    gid = os.getenv("DOCKER_NOTEBOOK_GROUPID")
    if not gid:
        gid = auth_state.get("gidNumber", [1000])[0]
        # Default to 1000 if gidNumber is not in auth_state

    spawner.environment.update(
        {
            "USERID": str(uid),
            "GROUPID": str(gid),
            "NB_UID": str(uid),
            "NB_GID": str(gid),
        }
    )
    spawner.log.info(
        f"Setting USERID and NB_UID to {uid} and GROUPID and NB_GID to {gid} for user {spawner.user.name}"
    )
