# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Poplddecay(MakefilePackage):
    """
    PopLDdecay: a fast and effective tool for linkage disequilibrium
    decay analysis based on variant call format files
    """

    homepage = "https://github.com/BGI-shenzhen/PopLDdecay"
    url = "https://github.com/BGI-shenzhen/PopLDdecay/archive/v3.41.tar.gz"

    maintainers("robqiao")

    license("MIT")

    version("3.41", sha256="b84fe5c9a1e1f6798eebbe4445b0b4bc7d02ac9f03fd01cb9cdcc8ee4db71040")
    version("3.40", sha256="5070930166fb90f7eaaa4b87c4430caa8a827d79c54683e2f56434a4daf69778")

    build_directory = "src"

    build_targets = ["all", "clean"]

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
