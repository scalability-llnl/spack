{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN yum update -y \
 && yum install -y epel-release \
 && yum update -y \
 && yum --enablerepo epel groupinstall -y "Development Tools" \
 && yum --enablerepo epel install -y \
        curl \
        findutils \
        gcc-c++ \
        gcc \
        gcc-gfortran \
        git \
        gnupg2 \
        hostname \
        iproute \
        make \
        patch \
        python \
        python-pip \
        python-setuptools \
        unzip \
 && pip install boto3 \
 && rm -rf /var/cache/yum \
 && yum clean all
{% endblock %}
