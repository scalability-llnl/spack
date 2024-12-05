# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kealib(CMakePackage):
    """An HDF5 Based Raster File Format.

    KEALib provides an implementation of the GDAL data model.
    The format supports raster attribute tables, image pyramids,
    meta-data and in-built statistics while also handling very
    large files and compression throughout.

    Based on the HDF5 standard, it also provides a base from which
    other formats can be derived and is a good choice for long
    term data archiving. An independent software library (libkea)
    provides complete access to the KEA image format and a GDAL
    driver allowing KEA images to be used from any GDAL supported software.

    Development work on this project has been funded by Landcare Research.
    """

    homepage = "http://www.kealib.org/"
    url = "https://github.com/ubarsc/kealib/releases/download/kealib-1.5.3/kealib-1.5.3.tar.gz"
    git = "https://github.com/ubarsc/kealib"

    maintainers("gillins", "neilflood", "petebunting")

    license("MIT")

    version("develop", git=git)
    version("1.5.3", sha256="32b2e3c90553a03cf1e8d03781c3710500ca919bca674bc370e86f15338ee93e")
    version("1.5.2", sha256="c4e17c472761a39e45184b5fa687395b319ac75430e0f6584dbf4cec6e335572")
    version("1.5.1", sha256="06cd547b1e40394b9539beaf6982bd249e8ee93d6150295e9cd9161d00829657")
    version("1.5.0", sha256="d19a0fb051019f87fe413bda76472bf4fff8fca52ede92e0ffd983caeafd05b8")
    version("1.4.15", sha256="40f2573c00f005f93c1fa88f1f13bfbd485cbc7a9b3f1c706931e69bff17dae4")
    version("1.4.12", sha256="0b100e36b3e25e57487aa197d7be47f22e1b30afb16a57fdaa5f877696ec321e")
    version("1.4.11", sha256="3d64cdec560c7a338ccb38e3a456db4e3b176ac62f945daa6e332e60fe4eca90")
    version("1.4.10", sha256="b1bd2d6834d2fe09ba456fce77f7a9452b406dbe302f7ef1aabe924e45e6bb5e")
    version("1.4.9", sha256="1c80489f17114a229097c2e8c61d5e4c82ea63ae631c81a817fef95cfd527174")
    version("1.4.8", sha256="0f24d8478865abcb17865c8f49c0370095726c529b8ac373ffae018ad3d40a02")
    version("1.4.7", sha256="ec38751b3b555d3a26f0c7445f2d2cd9d7c3a3502237519a206a50cb58df56ec")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build")
    depends_on("hdf5+cxx+hl", when="@:1.5.1")
    depends_on("hdf5+cxx", when="@1.5.2:")

    patch("cmake.patch", when="@1.4.7")

    @property
    def command(self):
        exe = "kea-config"
        if self.spec.satisfies("platform=windows"):
            exe += ".bat"
        return Executable(self.prefix.bin.join(exe))

    @property
    def root_cmakelists_dir(self):
        if self.version >= Version("1.4.9"):
            return "."
        else:
            return "trunk"

    def cmake_args(self):
        spec = self.spec

        if self.version >= Version("1.4.9"):
            return ["-DHDF5_ROOT={0}".format(spec["hdf5"].prefix)]
        else:
            return [
                "-DHDF5_INCLUDE_DIR={0}".format(spec["hdf5"].headers.directories[0]),
                "-DHDF5_LIB_PATH={0}".format(spec["hdf5"].libs.directories[0]),
            ]

    @property
    def libs(self):
        return find_libraries("libkea", self.prefix, shared=True, recursive=True)
