#! /usr/bin/env bash
#
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

mode=oneshot

if [ "$( basename "$0" )" '=' 'spack-env' ] ; then
    mode=spackenv
elif [ "$( basename "$0" )" '=' 'docker-shell' ] ; then
    mode=dockershell
elif [ "$( basename "$0" )" '=' 'interactive-shell' ] ; then
    mode=interactiveshell
elif [ "$1" '=' 'docker-shell' ] ; then
    mode=dockershell
    shift
elif [ "$1" '=' 'interactive-shell' ] ; then
    mode=interactiveshell
    shift
fi

case "$mode" in
    "spackenv")
        # Scenario 1: Run as if the image had no ENTRYPOINT
        #
        # Necessary for use cases where the command to run and all
        # arguments must be accepted in the CMD portion. (e.g.: Gitlab CI
        # Runners)
        #
        # Roughly equivalent to
        #   docker run ... --entrypoint spack-env ... sh -c "..."
        #
        # The shell script runs with spack pre-loaded and ready to use.
        . $SPACK_ROOT/share/spack/setup-env.sh
        unset CURRENTLY_BUILDING_DOCKER_IMAGE
        exec "$@"
        ;;

    "dockershell")
        # Scenario 2: Accept shell code from a RUN command in a
        # Dockerfile
        #
        # For new Docker images that start FROM this image as its base.
        # Prepared so that subsequent RUN commands can take advantage of
        # Spack without having to manually (re)initialize.
        #
        # Example:
        #   FROM spack/centos7
        #   COPY spack.yaml .
        #   RUN spack install  # <- Spack is loaded and ready to use.
        #                      # No manual initialization necessary.
        . $SPACK_ROOT/share/spack/setup-env.sh
        exec bash -c "$*"
        ;;

    "interactiveshell")
        # Scenario 3: Run an interactive shell session with Spack
        # preloaded.
        #
        # Create a container meant for an interactive shell session.
        # Additional checks are performed to ensure that stdin is a tty
        # and additional shell completion files are sourced.  The user is
        # presented with a shell prompt from which they may issue Spack
        # commands.
        #
        # This is the default behavior when running with no CMD or
        # ENTRYPOINT overrides:
        #   docker run -it spack/centos7
        if [ -t 0 ] ; then
            . $SPACK_ROOT/share/spack/setup-env.sh
            . $SPACK_ROOT/share/spack/spack-completion.bash
            unset CURRENTLY_BUILDING_DOCKER_IMAGE
            exec bash -i
        else
            (
                echo -n "It looks like you're trying to run an"
                echo -n " intractive shell session, but either no"
                echo -n " psuedo-TTY is allocated for this container's"
                echo    " STDIN, or it is closed."
                echo

                echo -n "Make sure you run docker with the --interactive"
                echo -n " and --tty options."
                echo
            ) >&2

            exit 1
        fi
        ;;

    "oneshot")
        # Scenario 4: Run a one-shot Spack command from the host command
        # line.
        #
        # Triggered by providing arguments to `docker run`.  Arguments
        # are passed along to the container's underlying spack
        # installation, allowing users to use the image as if it were
        # spack, itself.  Pass volume mount information to `docker run`
        # to persist the effects of running in this mode.
        #
        # This is the default behavior when running with a CMD override.
        #
        # Examples:
        #   # concretize the same spec on different OSes
        #   docker run --rm spack/ubuntu-xenial spec zlib
        #   docker run --rm spack/centos7 spec zlib
        #
        #   # a "wetter" dry-run;
        #   # install a package and then throw away the results.
        #   docker run --rm spack/centos7 install libiconv
        #   docker run --rm spack/centos7 find libiconv
        #     ==> No package matches the query: libiconv
        #
        #   # use docker volumes to persist changes
        #   docker run --rm -v ...:/spack spack/centos7 install ...
        #   docker run --rm -v ...:/spack spack/centos7 install ...
        #   docker run --rm -v ...:/spack spack/centos7 install ...
        exec 3>&1
        exec 4>&2

        exec 1>&-
        exec 2>&-

        . $SPACK_ROOT/share/spack/setup-env.sh
        unset CURRENTLY_BUILDING_DOCKER_IMAGE

        exec 1>&3
        exec 2>&4

        exec 3>&-
        exec 4>&-

        spack "$@"
        exit $?
        ;;

    *)
        echo "INTERNAL ERROR - UNRECOGNIZED MODE: $mode" >&2
        exit 1
        ;;
esac
