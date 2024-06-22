ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:${JUPYTERHUB_VERSION}

WORKDIR /srv/jupyterhub

COPY ./requirements/jupyterhub.txt .

# Install JupyterHub dependencies
ARG HTTP_PROXY
RUN if [ -z "$HTTP_PROXY" ] ; then \
    pip install --no-cache-dir -r jupyterhub.txt ; \
else \
    pip install --proxy=$HTTP_PROXY --no-cache-dir -r jupyterhub.txt ; \
fi && \
rm jupyterhub.txt

# Copy the JupyterHub configuration files
COPY ./config/jupyterhub/*.py /srv/jupyterhub/

ENV PYTHONPATH "${PYTHONPATH}:/srv/jupyterhub"

# Create a new user 'jupyterhub' and group 'docker'
# with the same gid as in the host machine.
# This avoids running the container as root and still allow
# access to the Docker socket.
ARG DOCKER_GID=1000
RUN addgroup --gid ${DOCKER_GID} docker && \
    adduser --disabled-password --gecos "" --gid ${DOCKER_GID} jupyterhub && \
    chown -R jupyterhub:docker /srv/jupyterhub

USER jupyterhub
