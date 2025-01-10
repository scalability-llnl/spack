{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN zypper ref && \
    zypper up -y && \
    zypper in -y \
    bzip2\
    curl\
    file\
    gcc-c++\
    gcc-fortran\
    make\
    mercurial\
    git\
    gzip\
    patch\
    python3-base \
    python3-boto3\
    subversion\
    tar\
    unzip\
    xz\
    zstd\
&&  zypper clean
{% endblock %}
