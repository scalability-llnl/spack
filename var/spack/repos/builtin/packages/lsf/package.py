# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Lsf(Package):
    """IBM Platform LSF is a batch scheduler for HPC environments"""

    homepage = "https://www.ibm.com/products/hpc-workload-management"
    has_code = False

    version("10.1")

    # LSF needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   lsf:
    #     buildable: False
    #     externals:
    #     - spec: lsf@10.1
    #       prefix: /usr/local/lsf/10.1 (path to your LSF installation)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
