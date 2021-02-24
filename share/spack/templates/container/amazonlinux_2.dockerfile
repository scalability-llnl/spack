{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN yum update -y \
 && yum groupinstall -y "Development Tools" \
 && yum install -y \
        curl \
        findutils \
        gcc-c++ \
        gcc \
        gcc-gfortran \
        git \
        gnupg2 \
        hostname \
        iproute \
        Lmod \
        make \
        patch \
        python \
        python-pip \
        python-setuptools \
        tcl \
        unzip \
        which \
 && pip install boto3 \
 && rm -rf /var/cache/yum \
 && yum clean all
{% endblock %}
