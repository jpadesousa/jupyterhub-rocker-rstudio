import os
from distutils.util import strtobool


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
