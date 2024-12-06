# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBcbioGff(PythonPackage):
    """Read and write Generic Feature Format (GFF) with Biopython
    integration."""

    pypi = "bcbio-gff/bcbio-gff-0.6.2.tar.gz"

    version("0.7.0", sha256="f7b3922ee274106f8716703f41f05a1795aa9d73e903f4e481995ed8f5f65d2d")
    version("0.6.2", sha256="c682dc46a90e9fdb124ab5723797a5f71b2e3534542ceff9f6572b64b9814e68")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
