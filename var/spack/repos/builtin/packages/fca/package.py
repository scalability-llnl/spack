# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fca(Package):
    """Legacy interface for Mellanox Fabric Collective Accelerator (FCA). FCA
    is a MPI-integrated software package that utilizes CORE-Direct technology
    for implementing the MPI collective communications."""

    homepage = "https://www.mellanox.com/products/fca"
    has_code = False

    version("2.5.2431")

    # FCA needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   fca:
    #     buildable: False
    #     externals:
    #     - spec: fca@2.5.2431
    #       prefix: /opt/mellanox/fca (path to your FCA installation)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
