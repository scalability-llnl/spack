# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mothur(MakefilePackage):
    """This project seeks to develop a single piece of open-source, expandable
    software to fill the bioinformatics needs of the microbial ecology
    community."""

    homepage = "https://github.com/mothur/mothur"
    url = "https://github.com/mothur/mothur/archive/v1.39.5.tar.gz"

    license("GPL-3.0-or-later")

    version("1.48.0", sha256="9494406abd8d14b821782ab9db811f045ded9424f28f01234ee6764d4e78941d")
    version("1.46.1", sha256="29b500b3c92d726cde34922f697f2e47f0b7127d76d9a6fb167cc2b8ba3d00fd")
    version("1.43.0", sha256="12ccd95a85bec3bb1564b8feabd244ea85413973740754803d01fc71ecb0a2c1")
    version("1.42.1", sha256="6b61591dda289ac2d8361f9c1547ffbeeba3b9fbdff877dd286bad850bbd5539")
    version("1.40.5", sha256="a0fbdfa68b966d7adc4560e3787506a0dad8b47b4b996c2663cd6c0b416d101a")
    version("1.39.5", sha256="9f1cd691e9631a2ab7647b19eb59cd21ea643f29b22cde73d7f343372dfee342")

    depends_on("cxx", type="build")  # generated
    maintainers("snehring")

    variant(
        "boost",
        default=True,
        description="Build with boost support (allow make.contigs to read gz files).",
    )
    variant("hdf5", default=False, description="Build with hdf5 support", when="@1.41.0:")
    variant(
        "gsl", default=False, description="Build with the gnu scientific libaries", when="@1.43.0:"
    )

    depends_on("boost+iostreams+filesystem+system", when="+boost")
    depends_on("gsl", when="+gsl")
    depends_on("hdf5+cxx", when="+hdf5")
    depends_on("readline")
    depends_on("vsearch@2.13.5:", type="run")
    depends_on("usearch", type="run")
    depends_on("zlib-api", when="+boost")

    def edit(self, spec, prefix):
        filter_file(r"^.*DMOTHUR_TOOLS.*$", "", "Makefile")
        filter_file(r"^.*DMOTHUR_FILES.*$", "", "Makefile")
        filter_file(r"(\$\(skipUchime\))", r"\1, source/", "Makefile")
        if spec.satisfies("@1.40.5"):
            filter_file(
                r"^(#define writer_h)", "\\1 \n#include<memory>", join_path("source", "writer.h")
            )
        # this includes the public domain uchime, which needs work to
        # compile on newer compilers we'll use what's in usearch
        filter_file(" uchime", "", "Makefile")
        if spec.satisfies("+boost"):
            filter_file(r"USEBOOST \?=.*$", "USEBOOST = yes", "Makefile")
            filter_file(
                r"^BOOST_LIBRARY_DIR .*$",
                "BOOST_LIBRARY_DIR=%s" % self.spec["boost"].prefix.lib,
                "Makefile",
            )
            filter_file(
                r"BOOST_INCLUDE_DIR .*$",
                "BOOST_INCLUDE_DIR=%s" % self.spec["boost"].prefix.include,
                "Makefile",
            )
        if spec.satisfies("+hdf5"):
            filter_file(r"USEHDF5 \?=.*$", "USEHDF5 = yes", "Makefile")
            filter_file(
                r"^HDF5_LIBRARY_DIR \?=.*$",
                "HDF5_LIBRARY_DIR = " + spec["hdf5"].prefix.lib,
                "Makefile",
            )
            filter_file(
                r"^HDF5_INCLUDE_DIR \?=.*$",
                "HDF5_INCLUDE_DIR = " + spec["hdf5"].prefix.include,
                "Makefile",
            )
        if spec.satisfies("+gsl"):
            filter_file(r"^USEGSL \?=.*$", "USEGSL = yes", "Makefile")
            filter_file(
                r"GSL_LIBRARY_DIR \?=.*$",
                "GSL_LIBRARY_DIR = " + spec["gsl"].prefix.lib,
                "Makefile",
            )
            filter_file(
                r"GSL_INCLUDE_DIR \?=.*$",
                "GSL_INCLUDE_DIR = " + spec["gsl"].prefix.include,
                "Makefile",
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("mothur", prefix.bin)
        install_tree("source", prefix.include)
