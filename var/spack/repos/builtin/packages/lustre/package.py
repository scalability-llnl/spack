# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Lustre(Package):
    """Lustre is a type of parallel distributed file system,
    generally used for large-scale cluster computing."""

    homepage = "http://lustre.org/"
    has_code = False

    executables = [r"^lfs$"]

    version("2.12")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"lfs (\d\S*)", output)
        return match.group(1) if match else None

    # Lustre is filesystem and needs to be installed on system.
    # To have it as external package in SPACK, follow below:
    # config file packages.yaml needs to be adjusted:
    #
    # packages:
    #   lustre:
    #     buildable: False
    #     externals:
    #     - spec: lustre@2.12
    #       prefix: /usr (Usual Lustre library path)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
