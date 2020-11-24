FROM opensuse/leap:15.2
MAINTAINER SUSE HPC <suse-hpc@suse.de>

ENV DOCKERFILE_BASE=opensuse          \
    DOCKERFILE_DISTRO=opensuse_leap   \
    DOCKERFILE_DISTRO_VERSION=15.2    \
    SPACK_ROOT_DOCKER=/opt/spack      \
    DEBIAN_FRONTEND=noninteractive    \
    CURRENTLY_BUILDING_DOCKER_IMAGE=1 \
    container=docker

COPY bin   $SPACK_ROOT/bin
COPY etc   $SPACK_ROOT/etc
COPY lib   $SPACK_ROOT/lib
COPY share $SPACK_ROOT/share
COPY var   $SPACK_ROOT/var


RUN mkdir -p $SPACK_ROOT/opt/spack

RUN 	zypper ref && \
	zypper up -y && \
	zypper in -y python3-base \
	xz gzip tar bzip2 curl patch \
	gcc-c++ make cmake automake&&\
  zypper clean

# clean up manpages
RUN	rm -rf /var/cache/zypp/*  \
	rm -rf /usr/share/doc/packages/* \ 
	rm -rf /usr/share/doc/manual/*


RUN mkdir -p /root/.spack \
 && cp $SPACK_ROOT/share/spack/docker/modules.yaml \
        /root/.spack/modules.yaml \
 && rm -rf /root/*.* /run/nologin $SPACK_ROOT/.git

# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
RUN [ -f ~/.profile ]                                               \
 && sed -i 's/mesg n/( tty -s \\&\\& mesg n || true )/g' ~/.profile \
 || true

WORKDIR /root
SHELL ["docker-shell"]

# Find tools which are in distro
RUN spack external find  --scope system

# TODO: add a command to Spack that (re)creates the package cache
RUN spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]


