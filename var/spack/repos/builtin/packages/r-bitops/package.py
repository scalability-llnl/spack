# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RBitops(RPackage):
    """Functions for bitwise operations on integer vectors."""

    homepage = "https://cloud.r-project.org/package=bitops"
    url      = "https://cloud.r-project.org/src/contrib/bitops_1.0-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bitops"

    version('1.0-6', sha256='9b731397b7166dd54941fb0d2eac6df60c7a483b2e790f7eb15b4d7b79c9d69c')
