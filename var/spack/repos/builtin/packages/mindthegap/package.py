# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mindthegap(CMakePackage):
    """MindTheGap is a software that performs integrated detection and
    assembly of genomic insertion variants in NGS read datasets with
    respect to a reference genome."""

    homepage = "https://gatb.inria.fr/software/mind-the-gap/"
    git = "https://github.com/GATB/MindTheGap.git"

    maintainers("snehring")

    license("AGPL-3.0-only")

    version(
        "2.3.0", tag="v2.3.0", commit="fe85c308434a4ad1ae7977dad67e966abc2bf93e", submodules=True
    )
    version(
        "2.0.2", tag="v2.0.2", commit="8401af2a2bce9997396fbf0a04757ca7c887a1da", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build", when="@2.3.0")
    depends_on("cmake@2.6:", type="build", when="@2.0.2")

    depends_on("zlib-api")
