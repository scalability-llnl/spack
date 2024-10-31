# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flashdimmsim(Package):
    """FlashDIMMSim: a reasonably accurate flash DIMM simulator."""

    homepage = "https://github.com/slunk/FlashDIMMSim"
    git = "https://github.com/slunk/FlashDIMMSim.git"

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    build_directory = "src"

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make()  # build program
            make("libfdsim.so")  # build shared library

            mkdir(prefix.bin)
            mkdir(prefix.lib)
            mkdir(prefix.include)

            install_tree("ini", join_path(prefix, "ini"))
            install("FDSim", prefix.bin)
            install("libfdsim.so", prefix.lib)
            install("*.h", prefix.include)
