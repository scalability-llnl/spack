# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hcoll(Package):
    """Modern interface for Mellanox Fabric Collective Accelerator (FCA). FCA
    is a MPI-integrated software package that utilizes CORE-Direct technology
    for implementing the MPI collective communications."""

    homepage = "https://www.mellanox.com/products/fca"
    has_code = False

    # To get the version number
    # grep HCOLL_VERNO_STRING path/include/hcoll/api/hcoll_version.h
    version("4.8.3221")  # HPC-X 2.14/2.15, UCX 1.15
    version("4.8.3220")  # HPC-X 2.13, UCX 1.14
    version("4.8.3217")  # HPC-X 2.12, UCX 1.14
    version("4.7.3208")  # HPC-X 2.11, UCX 1.13
    version("4.7.3202")  # HPC-X 2.10, UCX 1.12
    version("4.7.3199")  # HPC-X 2.9, UCX 1.11
    version("3.9.1927")

    # ucx throws warnings when running alongside the wrong version of hcoll
    requires("ucx@1.15", when="@4.8.3221")
    requires("ucx@1.14", when="@4.8.3217:4.8.3220")
    requires("ucx@1.13", when="@4.7.3208")
    requires("ucx@1.12", when="@4.7.3202")
    requires("ucx@1.11", when="@4.7.3199")

    # HCOLL needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   hcoll:
    #     buildable: False
    #     externals:
    #     - spec: hcoll@3.9.1927
    #       prefix: /opt/mellanox/hcoll (path to your HCOLL installation)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
