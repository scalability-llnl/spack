FROM ubuntu:18.04 AS bootstrap

ENV SPACK_ROOT=/spack \
    FORCE_UNSAFE_CONFIGURE=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get -yqq update \
 && apt-get -yqq install \
     --no-install-recommends \
     --no-install-suggests \
        base-files \
        ca-certificates \
        curl \
        debianutils \
        file \
        g++ \
        gcc \
        less \
        libc-dev-bin \
        libc6-dev \
        locales \
        make \
        python3 \
        tar \
 && rm -rf /var/lib/apt/lists/*

COPY bin /spack/bin
COPY etc /spack/etc
COPY lib /spack/lib

COPY share/spack/csh /spack/share/spack/csh
COPY share/spack/docs /spack/share/spack/docs
COPY share/spack/logo /spack/share/spack/logo
COPY share/spack/qa /spack/share/spack/qa
COPY share/spack/setup-env.* /spack/share/spack/
COPY share/spack/spack-completion.bash /spack/share/spack
COPY share/spack/templates /spack/share/spack/templates

COPY share/spack/docker/*.* /spack/share/spack/docker/
COPY share/spack/docker/package-index /spack/share/spack/docker/package-index

COPY var /spack/var

COPY share/spack/docker/conf/0* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 0

COPY share/spack/docker/conf/1* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 1

COPY share/spack/docker/conf/2* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 2

COPY share/spack/docker/conf/3* /spack/share/spack/docker/conf/
RUN /spack/share/spack/docker/run-bootstrap.sh 3

 ### && spack clean -a \

WORKDIR /work

# binutils
# bzip2
# coreutils
# curl
# diffutils
# file
# git
# gmake
# gnupg
# gzip
# nano
# patch
# patchelf
# python
# py-boto3
# py-pip
# sed
# tar
# unzip
# xz




### FROM ubuntu:18.04
### MAINTAINER Spack Maintainers <maintainers@spack.io>
### 
### ENV SPACK_ROOT=/opt/spack \
###     FORCE_UNSAFE_CONFIGURE=1 \
###     DEBIAN_FRONTEND=noninteractive
### 
### # Needed from OS:
### #     less
### #     curl
### RUN apt-get -yqq update \
###  && apt-get -yqq install --no-install-recommends \
###         build-essential \
###         ca-certificates \
###         coreutils \
###         curl \
###         g++ \
###         gcc \
###         gfortran \
###         less \
###         make \
###         python3 \
###         python3-pip \
### \
### # Make "python" and "pip" point to "python3" and "pip3", respectively
###  && ( py3="$( which python3 )" \
###  &&   update-alternatives --install \
###           "$( dirname $py3 )/python" python "$py3" 1 ) \
###  && ( pip3="$( which pip3 )" \
###  &&   update-alternatives --install \
###           "$( dirname $pip3 )/pip" pip "$pip3" 1 ) \
### \
### # Installed from pip:
### #     boto3
###  && pip install boto3 \
###  && rm -rf /var/lib/apt/lists/*
### 
### # INSTALL AND BOOTSTRAP
### # Bootstrapped packages:
### #     zlib
### #     tcl
### #     environment-modules
### COPY bin $SPACK_ROOT/bin
### COPY etc $SPACK_ROOT/etc
### COPY lib $SPACK_ROOT/lib
### COPY share $SPACK_ROOT/share
### COPY var $SPACK_ROOT/var
### RUN mkdir -p /etc/spack \
###              /spack-bootstrap/sw \
###              /spack-bootstrap/modules \
###              /spack/cache \
###              /spack/modules \
###              /spack/stage \
###              /spack/sw \
###              /root/.spack \
###  && cp $SPACK_ROOT/share/spack/docker/config.yaml \
###        $SPACK_ROOT/share/spack/docker/modules.yaml \
###        /etc/spack \
###  && cp $SPACK_ROOT/share/spack/docker/bootstrap-config.yaml \
###        /root/.spack/config.yaml \
###  && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
###           /bin/docker-shell \
###  && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
###           /bin/interactive-shell \
###  && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
###           /bin/spack-env \
###  && rm -rf $SPACK_ROOT/.git \
### \
### # This should be the only time that we'd need to source the setup script
### # before running spack.  Once bootstrapped, we can rely on the
### # entrypoint script to ensure spack is always loaded and ready to run.
###  && ( . $SPACK_ROOT/share/spack/setup-env.sh \
###  ;    spack bootstrap \
###  ;    spack module tcl refresh --yes-to-all \
###  &&   spack clean -a ) \
### \
### # Set up spack to use the bootstrapped packages as a spack-chain
###  && cp $SPACK_ROOT/share/spack/docker/upstreams.yaml /etc/spack \
### \
### # [WORKAROUND]
### # https://superuser.com/questions/1241548/
### #     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
###  && for dir in /root /etc/skel ; do \
###       if [ '!' -f "$dir/.profile" ] ; then continue ; fi \
###  ;    sed -i 's/mesg n/(tty -s \&\& mesg n || true)/g' "$dir/.profile" \
###  ;    done \
### \
### # create unprivileged user
###  && addgroup --quiet --system --gid 1000 spack \
###  && adduser --quiet --system --home /home/spack --shell /bin/sh \
###         --disabled-password --uid 1000 --gid 1000 spack \
###  && rm -rf /root/*.* /root/.spack \
### \
### # [WORKAROUND]
### # Workaround an issue where nonprivileged user cannot install packages
### # because spack tries to create- and write to files under-
### #     $spack/var/spack/junit-report
### # TODO: report this issue
###  && rm -rf $SPACK_ROOT/var/spack/junit-report \
###  && mkdir /spack/junit-report \
###  && ln -s /spack/junit-report $SPACK_ROOT/var/spack/junit-report \
### \
### # [END OF WORKAROUND]
###  && chown -R spack:spack /spack
### 
### USER spack
### WORKDIR /home/spack
### 
### SHELL ["docker-shell"]
### 
### ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
### CMD ["interactive-shell"]
