# jupyterhub-rocker-rstudio

![Demo Animation](assets/demo.gif "Demo")

## Description

This repository offers a deployment solution for [JupyterHub](https://jupyter.org/hub) on a server utilized by a small team, leveraging Docker to spawn images from [The Rocker Project](https://rocker-project.org/). The primary objective is to facilitate the management of multiple concurrent R versions, enabling users to select the appropriate version for their projects. Furthermore, Rocker Docker images apply a timestamp to R package installations, ensuring consistency by aligning package versions with the Docker image version.
