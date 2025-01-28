{% extends "container/bootstrap-base.dockerfile" %}
{% block env_vars %}
{{ super() }}
ENV DEBIAN_FRONTEND=noninteractive   \
    LANGUAGE=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8
{% endblock %}
{% block install_os_packages %}
RUN apt-get -yqq update \
 && apt-get -yqq upgrade \
 && apt-get -yqq install --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        file \
        g++ \
        gcc \
        gfortran \
        git \
        gnupg2 \
        iproute2 \
        locales \
        make \
        mercurial \
        subversion \
        python3 \
        python3-boto3 \
        unzip \
        zstd \
 && locale-gen en_US.UTF-8 \
 && rm -rf /var/lib/apt/lists/*
{% endblock %}
