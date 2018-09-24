#! /usr/bin/env bash

script="$( basename "$0" )"
cd "$( dirname "$0" )"

if [ -z "$BASE_IMAGE" ] ; then
    BASE_IMAGE="ubuntu"
fi

if [ -z "$BASE_TAG" ] ; then
    BASE_TAG="latest"
fi

if [ -z "$DISTRO" ] ; then
    DISTRO="${BASE_IMAGE}"
fi

if [ -z "$BASE_NAME" ] ; then
    BASE_NAME="${DISTRO}"
fi

if [ "$BASE_TAG" '=' 'latest' ] ; then
    BASE_TAG=""
fi

if [ -n "$BASE_TAG" ] ; then
    BASE_TAG=":${BASE_TAG}"
fi

TAG="spack/${BASE_NAME}${BASE_TAG}"

if [ "$script" '=' 'run-image.sh' ] ; then
    com="docker run --rm -ti"

    if [ -z "$DISABLE_MOUNT" ] ; then
        DISABLE_MOUNT=1
        if [ -z "$*" ] ; then
            DISABLE_MOUNT=0
        fi
    fi

    if [ "$DISABLE_MOUNT" '==' 0 ] ; then
        com="${com} -v \"$( readlink -f ../../.. ):/spack\""
    fi

    eval "exec ${com}" "${TAG}" "$@"
elif [ "$script" '=' 'push-image.sh' ] ; then
    docker push "${TAG}"
    for tag in ${EXTRA_TAGS} ; do
        docker push "spack/${BASE_NAME}:${tag}"
    done
else
    tag_options="-t ${TAG}"
    for tag in ${EXTRA_TAGS} ; do
        tag_options="${tag_options} -t spack/${BASE_NAME}:${tag}"
    done

    exec docker build -f ./Dockerfile                             \
                      ${tag_options}                              \
                      --build-arg BASE="${BASE_IMAGE}${BASE_TAG}" \
                      --build-arg DISTRO="${DISTRO}"              \
                      ../../..
fi
