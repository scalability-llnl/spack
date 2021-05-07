{% extends "container/ubuntu_1604.dockerfile" %}
{% block post_checkout %}
# [WORKAROUND]
# https://bugs.launchpad.net/ubuntu/+source/lua-posix/+bug/1752082
RUN ln -s posix_c.so /usr/lib/x86_64-linux-gnu/lua/5.2/posix.so
{% endblock %}
