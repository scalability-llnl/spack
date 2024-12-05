# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mxm(Package):
    """Mellanox Messaging Accelerator (MXM) provides enhancements to parallel
    communication libraries by fully utilizing the underlying networking
    infrastructure provided by Mellanox HCA/switch hardware."""

    homepage = "https://www.mellanox.com/products/mxm"
    has_code = False

    version("3.6.3104")

    # MXM needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   mxm:
    #     buildable: False
    #     externals:
    #     - spec: mxm@3.6.3104
    #       prefix: /opt/mellanox/mxm (path to your MXM installation)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
