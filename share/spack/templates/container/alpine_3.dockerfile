{% extends "container/bootstrap-base.dockerfile" %}
{% block install_os_packages %}
RUN apk update \
 && apk add --no-cache curl findutils gcc g++ gfortran git gnupg \
        make patch python3 py3-pip tcl unzip bash \
 && pip3 install boto3
{% endblock %}
