ARG IMAGE_TAG
ARG IMAGE_NAME

FROM ${IMAGE_NAME}:${IMAGE_TAG}

# Add a group and assign the user to that group
ARG GROUP_ID=1000
ARG GROUP_NAME=rstudio
ARG USER_ID=1000
USER root
RUN groupadd -g ${GROUP_ID} ${GROUP_NAME} || true && \
    usermod -u ${USER_ID} -g ${GROUP_ID} rstudio

# Update the package list and install necessary dependencies for pyenv and Python build
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

USER rstudio
WORKDIR /home/rstudio

# Set environment variables
ENV HOME /home/rstudio
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Set environment variables for proxy
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG FTP_PROXY
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
ENV ftp_proxy=${FTP_PROXY}

# Change Renviron.site
ARG R_LIBS=""
ARG R_HISTSIZE=1000
ARG R_TMPDIR=/tmp

USER root
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
USER rstudio

# Install pyenv
RUN curl https://pyenv.run | bash

ARG PYTHON_VERSION
RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION

# Install JupyterHub
ARG JUPYTERHUB_VERSION
RUN pip install jupyterhub==${JUPYTERHUB_VERSION}

# Install the packages specified in the requirements file
COPY ./requirements/rstudio.txt .
RUN pip install --no-cache-dir -r rstudio.txt && \
    rm rstudio.txt

# Update the PATH environment variable for the 'rstudio' user
RUN echo 'export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

CMD [ "jupyterhub-singleuser" ]
