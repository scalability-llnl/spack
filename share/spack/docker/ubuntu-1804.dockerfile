FROM ubuntu:18.04 AS base

ENV FORCE_UNSAFE_CONFIGURE=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get -yqq update \
 && apt-get -yqq install \
     --no-install-recommends \
     --no-install-suggests \
        base-files \
        ca-certificates \
        debianutils \
        less \
        libc-dev-bin \
        libc6-dev \
        locales \
 && locale-gen en_US.UTF-8 \
 && rm -rf /var/lib/apt/lists/*

ENV LANGUAGE=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

FROM base AS bootstrap

ENV SPACK_ROOT=/spack

RUN apt-get -yqq update \
 && apt-get -yqq install \
     --no-install-recommends \
     --no-install-suggests \
        curl \
        file \
        g++ \
        gcc \
        make \
        python3 \
        tar \
 && rm -rf /var/lib/apt/lists/*

COPY bin   /spack/bin
COPY etc   /spack/etc
COPY lib   /spack/lib
COPY share /spack/share
COPY var   /spack/var

RUN . /spack/share/spack/setup-env.sh \
 && if [ -z "$SPACK_SYS" ] ; then \
      eval "$( spack --print-shell-vars sh )" \
  ;   SPACK_SYS="$( echo $_sp_compatible_sys_types | sed 's/.*://g' )" \
  ; fi \
 && mkdir -p /etc/spack $HOME/.spack \
 && ( echo '---' \
 &&   echo 'config:' \
 &&   echo '  build_stage: /spack/stage' \
 &&   echo '  source_cache: /spack/cache' \
 &&   echo '  install_tree: /spack/sw' \
 &&   echo '  module_roots:' \
 &&   echo '    tcl: /spack/modules' ) > /etc/spack/config.yaml \
 && ( echo '---' \
 &&   echo 'modules:' \
 &&   echo '  tcl:' \
  ;   scheme='{name}/{version}-{compiler.name}{compiler.version}' \
 &&   echo '    naming_scheme: "'$scheme'"' \
 &&   echo '    hash_length: 4' \
 &&   echo '    all:' \
 &&   echo '      conflict:' \
 &&   echo '        - "{name}"' ) > /etc/spack/modules.yaml \
 && ( echo '---' \
 &&   echo 'config:' \
 &&   echo '  install_tree: /spack-prebootstrap/sw' \
 &&   echo '  module_roots:' \
 &&   echo '    tcl: /spack-prebootstrap/modules' ) > $HOME/.spack/config.yaml \
 && spack repo add --scope user /spack/share/spack/docker/bootstrap-repo \
 && spack bootstrap \
 && spack module tcl refresh --yes-to-all \
 && spack install --only dependencies spack-bootstrap@1 "arch=$SPACK_SYS" \
 && spack view --dependencies no symlink /usr/local tar xz \
 && spack install --only dependencies spack-bootstrap@2 "arch=$SPACK_SYS" \
 && spack view --dependencies no symlink /usr/local gzip patch sed unzip \
 && ( echo '---' \
 &&   echo 'config:' \
 &&   echo '  install_tree: /spack-bootstrap/sw' \
 &&   echo '  module_roots:' \
 &&   echo '    tcl: /spack-bootstrap/modules' ) > $HOME/.spack/config.yaml \
 && spack install --only dependencies spack-bootstrap@3 "arch=$SPACK_SYS" \
 && spack view --dependencies no symlink /usr/local gcc \
 && spack compiler find \
 && ( echo '---' \
 &&   echo 'upstreams:' \
 &&   echo '  spack-bootstrap:' \
 &&   echo '    install_tree: /spack-bootstrap/sw' \
 &&   echo '    modules:' \
 &&   echo '      tcl: /spack-bootstrap/modules' ) > /etc/spack/upstreams.yaml \
 && spack install --only dependencies spack-bootstrap@4 "arch=$SPACK_SYS" \
 && spack view --dependencies no symlink /usr/local git \
 && spack install --only dependencies spack-bootstrap@5 "arch=$SPACK_SYS" \
 && spack view --dependencies no symlink /usr/local \
        binutils \
        bzip2 \
        coreutils \
        curl \
        diffutils \
        file \
        gmake \
        gnupg \
        nano \
        patchelf \
        python \
        py-boto3 \
        py-pip \
 && spack clean -a \
 && rm -rf /spack/cache /spack/var/spack/cache

FROM base

MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV SPACK_ROOT=/opt/spack

COPY --from=bootstrap /spack /opt/spack

RUN ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/docker-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/interactive-shell \
 && ln -s $SPACK_ROOT/share/spack/docker/entrypoint.bash \
          /usr/local/bin/spack-env \
\
# [WORKAROUND]
# https://superuser.com/questions/1241548/
#     xubuntu-16-04-ttyname-failed-inappropriate-ioctl-for-device#1253889
 && for dir in /root /etc/skel ; do \
      if [ '!' -f "$dir/.profile" ] ; then continue ; fi \
 ;    sed -i 's/mesg n/(tty -s \&\& mesg n || true)/g' "$dir/.profile" \
 ;    done \
\
# create unprivileged user
 && addgroup --quiet --system --gid 1000 spack \
 && adduser --quiet --system --home /home/spack --shell /bin/sh \
        --disabled-password --uid 1000 --gid 1000 spack \
\
# [WORKAROUND]
# Workaround an issue where nonprivileged user cannot install packages
# because spack tries to create- and write to files under-
#     $spack/var/spack/junit-report
#   (/spack is given to "spack" user below)
# TODO: report this issue
 && rm -rf $SPACK_ROOT/var/spack/junit-report \
 && mkdir -p /spack/junit-report \
 && ln -s /spack/junit-report $SPACK_ROOT/var/spack/junit-report

COPY --from=bootstrap /etc/spack /etc/spack
COPY --from=bootstrap /spack-bootstrap /spack-bootstrap

RUN ln -s /spack-bootstrap/sw/*/*/file*/bin/file /usr/bin/file \
 && ln -s /spack-bootstrap/sw/*/*/python*/bin/python /usr/bin/python \
 && /opt/spack/bin/spack view symlink /usr/local \
      bzip2 \
      binutils \
      coreutils \
      curl \
      diffutils \
      file \
      git \
      gmake \
      gnupg \
      gzip \
      nano \
      patch \
      patchelf \
      python \
      py-boto3 \
      py-pip \
      sed \
      tar \
      unzip \
      xz \
 && /opt/spack/bin/spack view --dependencies no symlink /usr/local gcc \
 && chown -R spack:spack /spack \
 && rm -rf /usr/bin/file \
           /usr/bin/python \
           /root/*.* \
           /root/.spack \
\
           # Need to remove the symlinked libintl.  Otherwise, the builds for
           # some packages with optional NLS support get terribly confused on
           # when & how to enable gettext().
           /usr/local/lib/libintl.*

SHELL ["docker-shell"]

USER spack
WORKDIR /home/spack

# TODO: add a command to Spack that (re)creates the package cache
RUN spack spec hdf5+mpi

ENTRYPOINT ["/bin/bash", "/opt/spack/share/spack/docker/entrypoint.bash"]
CMD ["interactive-shell"]
