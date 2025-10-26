
FROM mcr.microsoft.com/devcontainers/python:3.10

ENV PYTHONUNBUFFERED 1

# install needed system packages to build python extensions
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
       build-essential libpq-dev python3-dev pkg-config libffi-dev libssl-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# install pipenv to support the project's Pipfile if used
RUN pip3 install --no-cache-dir pipenv

# copy requirements and install at image build time so the devcontainer has deps ready after rebuild
COPY requirements.txt /tmp/requirements.txt
# Prefer a minimal requirements file during the image build if available
# to avoid build failures caused by pinned/old packages in the full requirements.
COPY requirements_minimal.txt /tmp/requirements_minimal.txt
RUN if [ -s /tmp/requirements_minimal.txt ]; then \
            pip3 install --no-cache-dir -r /tmp/requirements_minimal.txt || true; \
        elif [ -s /tmp/requirements.txt ]; then \
            pip3 install --no-cache-dir -r /tmp/requirements.txt || true; \
        fi



