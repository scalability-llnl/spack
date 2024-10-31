# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5utils(AutotoolsPackage):
    """h5utils is a set of utilities for visualization and conversion of
    scientific data in the free, portable HDF5 format."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/H5utils"
    url = "https://github.com/NanoComp/h5utils/releases/download/1.13.1/h5utils-1.13.1.tar.gz"

    license("GPL-2.0-only")

    version("1.13.2", sha256="eea7855a8235facb7c454e61103098e55658da0ddf4b6de5b82a992e5f024351")
    version("1.13.1", sha256="c5a76f064d6daa3e65583dce2b61202510e67cf6590f076af9a8aa72511d7d65")
    version(
        "1.12.1",
        sha256="7e6db86fee00a8008f78b2be921177042c661203c0936b078fcc8f9c71e4a883",
        url="https://github.com/NanoComp/h5utils/archive/refs/tags/1.12.1.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("png", default=True, description="Enable PNG support")
    variant("vis5d", default=False, description="Enable Vis5d support")
    variant("octave", default=False, description="Enable GNU Octave support")
    variant("hdf4", default=False, description="Enable HDF4 support")
    variant("math", default=False, description="Build h5math")

    # Required dependencies
    depends_on("hdf5")

    # Optional dependencies
    depends_on("libpng", when="+png")
    depends_on("libpng@:1.5.0", when="@1.12.1+png")
    # depends_on('vis5d',       when='+vis5d')  # TODO: Add a vis5d package
    depends_on("octave", when="+octave")
    depends_on("hdf", when="+hdf4")
    depends_on("libmatheval", when="+math")

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("+vis5d"):
            args.append(f"--with-v5d={spec['vis5d'].prefix}")
        else:
            args.append("--without-v5d")

        if spec.satisfies("+octave"):
            args.append("--with-octave")
        else:
            args.append("--without-octave")

        if spec.satisfies("+hdf"):
            args.append("--with-hdf4")
        else:
            args.append("--without-hdf4")

        return args
