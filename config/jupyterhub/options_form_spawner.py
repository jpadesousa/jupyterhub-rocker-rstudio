import os
import json
from dockerspawner import DockerSpawner
from options_form_spawner_template import get_form_template


class OptionsFormSpawner(DockerSpawner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_images = os.getenv(
            "DOCKER_NOTEBOOKS", "jupyter/minimal-notebook:latest"
        ).split(",")
        self.server_options = {image: image for image in self.server_images}
        self.server_ports = json.loads(
            os.getenv("DOCKER_NOTEBOOK_PORTS", '{"jupyter/minimal-notebook": 10000}')
        )
        self.server_dir = json.loads(
            os.getenv(
                "DOCKER_NOTEBOOK_DIR",
                '{"jupyter/minimal-notebook": "/home/jovyan/work"}',
            )
        )
        self.volumes = {f"jupyterhub-user-{self.user.name}": self.server_dir}

        additional_volumes_str = os.getenv("DOCKER_NOTEBOOK_ADD_VOLUMES")
        if additional_volumes_str:
            additional_volumes = json.loads(additional_volumes_str)
            self.volumes.update(additional_volumes)

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

        return await super().start(*args, **kwargs)

    def get_form_options(self, server_options):
        return "\n".join(
            (f'<option value="{k}">{v}</option>' for k, v in server_options.items())
        )

    def _options_form_default(self):
        options = self.get_form_options(self.server_options)
        return get_form_template().format(options=options)
