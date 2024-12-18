# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Torque(Package):
    """TORQUE (Terascale Open-source Resource and QUEue Manager) is an open
    source project based on the original PBS resource manager developed by NASA,
    LLNL, and MRJ."""

    homepage = "https://github.com/abarbu/torque"
    has_code = False

    version("3.0.4")
    version("3.0.2")

    provides("pbs")

    # TORQUE needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   torque:
    #     buildable: False
    #     externals:
    #     - spec: torque@3.0.2
    #       prefix: /opt/torque (path to your TORQUE installation)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
