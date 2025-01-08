{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN dnf update -y \
 && dnf install -y \
        bzip2 \
        curl \
        file \
        findutils \
        gcc-c++ \
        gcc \
        gcc-gfortran \
        git \
        gnupg2 \
        hg \
        hostname \
        iproute \
        make \
        patch \
        python3 \
        python3-pip \
        python3-setuptools \
        svn \
        unzip \
        xz \
        zstd \
 && pip3 install boto3 \
 && rm -rf /var/cache/dnf \
 && dnf clean all
{% endblock %}
