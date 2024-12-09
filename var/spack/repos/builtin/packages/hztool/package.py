# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hztool(AutotoolsPackage):
    """HZTool is a library of routines which will allow you to reproduce an
    experimental result using the four-vector final state from Monte Carlo
    generators."""

    homepage = "https://hztool.hepforge.org"
    url = "https://hztool.hepforge.org/downloads/?f=hztool-4.3.2.tar.gz"
    list_url = "https://hztool.hepforge.org/downloads/"

    maintainers("wdconinc")

    tags = ["hep"]

    license("GPL-2.0-only")

    version("4.3.2", sha256="2a8d334abd96a7a9f70d53cfbb46f35902ccd1108861333a87542f8357152fd4")
    version("4.3", sha256="af1a302c16e9f0bfbfdd77a486a5f47553d81d1d049bc83cc72321ba285af264")
    version("4.2", sha256="87b74b2e424a1e6bd990cc12a0bfcba15854a6451ffa20aff8dc4bdfed559160")
    version("4.1", sha256="a24b5d483d1dacaa991958956e838601a426133c74885b3aa2fc27c98b42d22a")
    version("4.0", sha256="e6f6955159da46156bf9182f61754a59dd14e407d40c2448e3f821d55bf963a0")

    depends_on("fortran", type="build")  # generated

    def patch(self):
        filter_file("-fno-automatic", "-fno-automatic -fallow-argument-mismatch", "configure.ac")

    def configure_args(self):
        args = []
        args.append("--disable-docs")
        return args
