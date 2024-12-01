# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Rockstar(MakefilePackage):
    """The Rockstar Halo Finder"""

    homepage = "https://bitbucket.org/gfcstanford/rockstar"

    version("develop", git="https://bitbucket.org/gfcstanford/rockstar.git")
    version("yt", hg="https://bitbucket.org/MatthewTurk/rockstar")

    variant("hdf5", description="Build rockstar with HDF5 support", default=False)

    patch("adjust_buildscript.patch")

    depends_on("hdf5", when="+hdf5")

    def build(self, spec, prefix):
        # Set environment appropriately for HDF5
        if "+hdf5" in spec:
            os.environ["HDF5_INC_DIR"] = spec["hdf5"].prefix.include
            os.environ["HDF5_LIB_DIR"] = spec["hdf5"].prefix.lib

        # Build depending on whether hdf5 is to be used
        if "+hdf5" in spec:
            make("with_hdf5")
        else:
            make()

        # Build rockstar library
        make("lib")

    def install(self, spec, prefix):
        # Install all files and directories
        install_tree(".", prefix)

        mkdir(prefix.bin)
        mkdir(prefix.lib)

        install("rockstar", join_path(prefix.bin, "rockstar"))
        install("librockstar.so", join_path(prefix.lib, "librockstar.so"))
