# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ioapi(MakefilePackage):
    """Models-3/EDSS Input/Output Applications Programming Interface."""

    homepage = "https://www.cmascenter.org/ioapi/"
    url = "https://www.cmascenter.org/ioapi/download/ioapi-3.2.tar.gz"
    maintainers("omsai")
    # This checksum is somewhat meaningless because upstream updates the tarball
    # without incrementing the version despite requests no to do this.
    # Therefore the checksum fails everytime upstream silently updates the
    # source tarball (#28247).  This also means that one must test for breaking
    # changes when updating the checksum and avoid #22633.
    version("3.2", sha256="0a3cbf236ffbd9fb5f6509e35308c3353f1f53096efe0c51b84883d2da86924b")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("netcdf-c@4:")
    depends_on("netcdf-fortran@4:")
    depends_on("sed", type="build")

    def edit(self, spec, prefix):
        # No default Makefile bundled; edit the template.
        os.symlink("Makefile.template", "Makefile")
        # The makefile uses stubborn assignments of = instead of ?= so
        # edit the makefile instead of using environmental variables.
        makefile = FileFilter("Makefile")
        makefile.filter(
            "(^VERSION.*)",
            """
CPLMODE = nocpl
\\1
        """.strip(),
        )
        makefile.filter(
            "^BASEDIR.*",
            (
                """
BASEDIR = """
                + self.build_directory
                + """
INSTALL = """
                + prefix
                + """
BININST = """
                + prefix.bin
                + """
LIBINST = """
                + prefix.lib
                + """
BIN = Linux2_x86_64
        """
            ).strip(),
        )
        # Fix circular dependency bug for generating subdirectory Makefiles.
        makefile.filter("^configure:.*", "configure:")
        # Generate the subdirectory Makefiles.
        make("configure")

    def install(self, spec, prefix):
        make("install")
        # Install the header files.
        mkdirp(prefix.include.fixed132)
        install("ioapi/*.EXT", prefix.include)
        # Install the header files for CMAQ and SMOKE in the
        # non-standard -ffixed-line-length-132 format.
        install("ioapi/fixed_src/*.EXT", prefix.include.fixed132)
