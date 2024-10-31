#!/usr/bin/env bash
#
# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
set -e

set_pcluster_defaults() {
    # Set versions of pre-installed software in packages.yaml
    [ -z "${SLURM_ROOT}" ] && ls /etc/systemd/system/slurm* &>/dev/null && \
        SLURM_ROOT=$(dirname $(dirname "$(awk '/ExecStart=/ {print $1}' /etc/systemd/system/slurm* | sed -e 's?^.*=??1' | head -n1)"))
    # Fallback to default location if SLURM not in systemd
    [ -z "${SLURM_ROOT}" ] && [ -d "/opt/slurm" ] && SLURM_ROOT=/opt/slurm
    [ -z "${SLURM_VERSION}" ] && SLURM_VERSION=$(strings "${SLURM_ROOT}"/lib/libslurm.so | grep -e '^VERSION' | awk '{print $2}' | sed -e 's?"??g')
    [ -z "${LIBFABRIC_VERSION}" ] && LIBFABRIC_VERSION=$(awk '/Version:/{print $2}' "$(find /opt/amazon/efa/ -name libfabric.pc | head -n1)" | sed -e 's?~??g' -e 's?amzn.*??g')
    export SLURM_ROOT SLURM_VERSION LIBFABRIC_VERSION

    envsubst < "${SPACK_ROOT}/share/spack/gitlab/cloud_pipelines/stacks/${SPACK_CI_STACK_NAME}/packages.yaml" > "${SPACK_ROOT}"/etc/spack/packages.yaml
}

patch_compilers_yaml() {
    # Graceful exit if package not found by spack
    set -o pipefail
    compilers_yaml="${SPACK_ROOT}/etc/spack/compilers.yaml"
    [ -f "${compilers_yaml}" ] || {
        echo "Cannot find ${compilers_yaml}, compiler setup might now be optimal."
        return
    }

    # System ld is too old for amzn linux2
    spack_gcc_version=$(spack find --format '{version}' gcc)
    binutils_path=$(spack find -p binutils | awk '/binutils/ {print $2}' | head -n1)
    if [ -d "${binutils_path}" ] && [ -n "${spack_gcc_version}" ]; then python3 <<EOF
import yaml

with open("${compilers_yaml}",'r') as f:
    compilers=yaml.safe_load(f)

for c in compilers["compilers"]:
    if "arm" in c["compiler"]["spec"] or "intel" in c["compiler"]["spec"] or "oneapi" in c["compiler"]["spec"] \
       or "${spack_gcc_version}" in c["compiler"]["spec"]:
        compilers["compilers"][compilers["compilers"].index(c)]["compiler"]["environment"] = {"prepend_path":{"PATH":"${binutils_path}/bin"}}

with open("${compilers_yaml}",'w') as f:
    yaml.dump(compilers, f)
EOF
    fi
    # Oneapi needs extra_rpath to gcc libstdc++.so.6
    if [ "x86_64" == "$(arch)" ] && oneapi_gcc_version=$(spack find --format '{compiler}' intel-oneapi-compilers | sed -e 's/=//g') && \
            [ -n "${oneapi_gcc_version}" ] && oneapi_gcc_path=$(spack find -p "${oneapi_gcc_version}" | grep "${oneapi_gcc_version}" | awk '{print $2}' | head -n1) && \
            [ -d "${oneapi_gcc_path}" ]; then python3 <<EOF
import yaml

with open("${compilers_yaml}",'r') as f:
    compilers=yaml.safe_load(f)

for c in compilers["compilers"]:
    if "oneapi" in c["compiler"]["spec"]:
        compilers["compilers"][compilers["compilers"].index(c)]["compiler"]["extra_rpaths"] = ["${oneapi_gcc_path}/lib64"]

with open("${compilers_yaml}",'w') as f:
    yaml.dump(compilers, f)
EOF
    fi
}

install_compilers() {
    # Install Intel compilers through a static spack version such that the compiler's hash does not change.
    # The compilers needs to be in the same install tree as the rest of the software such that the path
    # relocation works correctly. This holds the danger that this part will fail when the current spack gets
    # incompatible with the one in $spack_intel_compiler_commit. Therefore, we make intel installations optional
    # in packages.yaml files and add a fallback `%gcc` version for each application.
    if [ -f "/bootstrap-compilers/spack/etc/spack/compilers.yaml" ]; then
        # Running inside a gitlab CI container
        # Intel and gcc@12 compiler are pre-installed and their location is known in 
        cp /bootstrap-compilers/spack/etc/spack/compilers.yaml "${SPACK_ROOT}"/etc/spack/
    else
        spack compiler add --scope site
        # We need to treat compilers as essentially external, i.e. their installation location
        # (including hash) must not change when any changes are pushed to spack. The reason is that
        # changes in the compilers are not reflected in the package hashes built in the CI. Hence, those
        # packages will reference a wrong compiler path once the path changes.

        # `gcc@12.4.0%gcc@7.3.1` is created as part of building the pipeline containers.
        # `ghcr.io/spack/pcluster-amazonlinux-2:v2024-10-07` produced the following hashes.
        if [ "x86_64" == "$(arch)" ]; then
            gcc_hash="pttzchh7o54nhmycj4wgzw5mic6rk2nb"
        else
            gcc_hash="v6wxye6ijzrxnzxftcwnpu3psohsjl2b"
        fi

        spack install /${gcc_hash}
        (
            spack load gcc
            spack compiler add --scope site
        )

        if [ "x86_64" == "$(arch)" ]; then
            # 2024.1.0 is the last oneapi compiler that works on AL2 and is the one used to compile packages in the build cache.
            spack install intel-oneapi-compilers@2024.1.0
            (
                . "$(spack location -i intel-oneapi-compilers)"/setvars.sh; spack compiler add --scope site \
                    || true
            )
        fi
    fi
}

set_pcluster_defaults
install_compilers
patch_compilers_yaml
