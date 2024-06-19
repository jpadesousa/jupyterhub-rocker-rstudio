ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:${JUPYTERHUB_VERSION}

WORKDIR /srv/jupyterhub

# Install JupyterHub dependencies
COPY ./requirements/jupyterhub.txt .
ARG PIP_PROXY
RUN if [ -z "$PIP_PROXY" ] ; then \
    pip install --no-cache-dir -r jupyterhub.txt ; \
else \
    pip install --proxy=$PIP_PROXY --no-cache-dir -r jupyterhub.txt ; \
fi

COPY ./config/jupyterhub/*.py /srv/jupyterhub/

ENV PYTHONPATH "${PYTHONPATH}:/srv/jupyterhub"
