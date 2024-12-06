import os


def auth_state_hook(spawner, auth_state):
    if not auth_state:
        spawner.log.info(f"No auth_state for user {spawner.user.name}")
        return

    # Get the uidNumber or agrlUidNumber from the auth_state
    uid = os.getenv("DOCKER_NOTEBOOK_USERID")
    if not uid:
        uid = auth_state.get("user_attributes", {}).get("uidNumber")
        if uid:
            uid = uid[0]
        else:
            uid = auth_state.get("user_attributes", {}).get("agrlUidNumber", [1000])[0]

    # Get the gidNumber or agrlGidNumber from the auth_state
    gid = os.getenv("DOCKER_NOTEBOOK_GROUPID")
    if not gid:
        gid = auth_state.get("user_attributes", {}).get("gidNumber")
        if gid:
            gid = gid[0]
        else:
            gid = auth_state.get("user_attributes", {}).get("agrlGidNumber", [1000])[0]

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
