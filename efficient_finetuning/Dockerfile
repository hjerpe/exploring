FROM mcr.microsoft.com/devcontainers/python:0-3.10

#USER root
# RUN apt update \
#    && DEBIAN_FRONTEND=noninteractive apt install -y \
#    rm -rf /var/lib/apt/lists/*
USER root
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y vim tree \
    && apt-get clean  # This line cleans up the package lists to reduce image size

ENV USER=vscode
USER $USER
# Install a GCP friendly python version (TODO check image above if it is GCP friendly).
# It will be installed side-by-side with the 3.9 version and managed by pyenv.
ENV PYENV_ROOT /home/$USER/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

WORKDIR /home/$USER
COPY ./.docker_requirements.txt .
RUN pip install -r .docker_requirements.txt
