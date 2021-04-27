# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RBrio(RPackage):
    """Basic R Input Output

    Functions to handle basic input output, these functions always read and
    write UTF-8 (8-bit Unicode Transformation Format) files and provide more
    explicit control over line endings."""

    homepage = "https://github.com/r-lib/brio"
    url      = "https://cloud.r-project.org/src/contrib/brio_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/brio"

    version('1.1.0', sha256='6bb3a3b47bea13f1a1e3dcdc8b9f688502643e4b40a481a34aa04a261aabea38')
