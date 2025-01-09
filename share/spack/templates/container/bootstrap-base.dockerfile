FROM {{ bootstrap.image }} AS bootstrap

{% block env_vars %}
ENV SPACK_ROOT=/opt/spack \
    CURRENTLY_BUILDING_DOCKER_IMAGE=1 \
    container=docker
{% endblock %}

{% block install_os_packages %}
{% endblock %}

RUN mkdir $SPACK_ROOT && cd $SPACK_ROOT && \
    {{ bootstrap.spack_checkout }} && \
    mkdir -p $SPACK_ROOT/opt/spack

RUN ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/docker-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/interactive-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/spack-env

RUN mkdir -p /root/.spack \
 && cp $SPACK_ROOT/share/spack/docker/modules.yaml \
        /root/.spack/modules.yaml \
 && rm -rf /root/*.* /run/nologin

# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
RUN [ -f ~/.profile ]                                               \
 && sed -i 's/mesg n/( tty -s \\&\\& mesg n || true )/g' ~/.profile \
 || true

{% block post_checkout %}
{% endblock %}

WORKDIR /root
SHELL ["docker-shell"]

# Creates the package cache
RUN spack bootstrap now \
    && spack bootstrap status --optional \
    && spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]
