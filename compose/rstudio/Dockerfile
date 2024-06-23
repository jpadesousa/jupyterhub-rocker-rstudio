# Base image
ARG IMAGE_TAG
ARG IMAGE_NAME
FROM ${IMAGE_NAME}:${IMAGE_TAG}

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    libgdal-dev \
    libgsl-dev \
    libhdf5-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libpq-dev \
    libproj-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libudunits2-dev \
    libzmq3-dev \
    libglpk-dev \
    libfftw3-3 \
    libsuitesparse-dev \
    llvm \
    make \
    nodejs \
    npm \
    openssl \
    python3-pip \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/rstudio

# Environment variables setup
ENV HOME /home/rstudio
ENV PYENV_ROOT /opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# R environment configuration
ARG R_LIBS=""
ARG R_HISTSIZE=1000
ARG R_TMPDIR=/tmp
RUN if [ -z "${R_LIBS}" ]; then \
        echo "R_LIBS=/usr/local/lib/R/site-library:/usr/local/lib/R/library" > $R_HOME/etc/Renviron.site; \
    else \
        echo "R_LIBS=${R_LIBS}:/usr/local/lib/R/site-library:/usr/local/lib/R/library" > $R_HOME/etc/Renviron.site; \
    fi && \
    echo "http_proxy=${HTTP_PROXY}" >> $R_HOME/etc/Renviron.site && \
    echo "https_proxy=${HTTPS_PROXY}" >> $R_HOME/etc/Renviron.site && \
    echo "ftp_proxy=${FTP_PROXY}" >> $R_HOME/etc/Renviron.site && \
    echo "R_HISTSIZE=${R_HISTSIZE}" >> $R_HOME/etc/Renviron.site && \
    echo "TMPDIR=${R_TMPDIR}" >> $R_HOME/etc/Renviron.site

# RStudio configuration
ARG COPILOT_ENABLED
RUN if [ "${COPILOT_ENABLED}" ]; then echo "copilot-enabled=${COPILOT_ENABLED}" >> /etc/rstudio/rsession.conf; fi

ARG STARTUP_MESSAGE
RUN if [ "${STARTUP_MESSAGE}" ]; then echo "message(${STARTUP_MESSAGE})" >> $R_HOME/etc/Rprofile.site; fi

# pyenv and Python setup
RUN curl https://pyenv.run | bash
ARG PYTHON_VERSION
RUN pyenv install $PYTHON_VERSION && \
    pyenv global $PYTHON_VERSION
RUN chown -R rstudio:rstudio /opt/pyenv

# JupyterHub installation
USER rstudio
ARG JUPYTERHUB_VERSION
RUN pip install --upgrade pip && \
    pip install jupyterhub==${JUPYTERHUB_VERSION}

# Python dependencies installation
COPY ./requirements/rstudio.txt .
RUN pip install --no-cache-dir -r rstudio.txt && \
    rm rstudio.txt

# Update PATH
RUN echo 'export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

# Final setup
USER root
RUN echo "exec su rstudio -c /opt/pyenv/shims/jupyterhub-singleuser" >> /init
CMD ["/init"]
