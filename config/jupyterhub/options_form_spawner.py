import os
import json
import re
from dockerspawner import DockerSpawner
from options_form_spawner_template import get_form_template


class OptionsFormSpawner(DockerSpawner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # List of the docker notebooks images
        self.server_images = os.getenv(
            "DOCKER_NOTEBOOKS", "jupyter/minimal-notebook:latest"
        ).split(",")
        self.server_options = {image: image for image in self.server_images}

        # List of docker notebook ports
        self.server_ports = json.loads(
            os.getenv("DOCKER_NOTEBOOK_PORTS", '{"jupyter/minimal-notebook": 8888}')
        )

        # Docker notebook default directory
        self.server_dir = json.loads(
            os.getenv(
                "DOCKER_NOTEBOOK_DIR",
                '{"jupyter/minimal-notebook": "/home/jovyan/work"}',
            )
        )

        # Add shared volumes between the host and the container
        add_volumes_str = os.getenv("DOCKER_NOTEBOOK_ADD_VOLUMES")
        if add_volumes_str:
            add_volumes = json.loads(add_volumes_str)
            self.volumes.update(add_volumes)

        # Jupyterhub default URL for the docker notebook
        self.server_default_url = json.loads(
            os.getenv(
                "DOCKER_NOTEBOOK_DEFAULT_URL", '{"jupyter/minimal-notebook": "/lab"}'
            )
        )

    def options_from_form(self, formdata):
        self.image = "".join(formdata["server"])
        return {}

    async def start(self, *args, **kwargs):
        base_image_name = self.image.split(":")[0]
        self.port = self.server_ports.get(base_image_name)
        self.notebook_dir = self.server_dir.get(base_image_name)
        self.volumes.update({f"jupyterhub-user-{self.user.name}": self.notebook_dir})
        self.default_url = self.server_default_url.get(base_image_name)

        # Starting the jupyter/*-notebook as root to change the uid and gid of the user
        if re.match(r"^jupyter/.+-notebook$", base_image_name):
            self.extra_create_kwargs.update({"user": "root"})
            self.environment["CHOWN_HOME"] = "yes"
            self.environment["CHOWN_HOME_OPTS"] = "-R"

        return await super().start(*args, **kwargs)

    def get_form_options(self, server_options):
        return "\n".join(
            (f'<option value="{k}">{v}</option>' for k, v in server_options.items())
        )

    def _options_form_default(self):
        options = self.get_form_options(self.server_options)
        return get_form_template().format(options=options)
