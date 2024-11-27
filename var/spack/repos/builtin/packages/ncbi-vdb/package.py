# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NcbiVdb(CMakePackage):
    """The SRA Toolkit and SDK from NCBI is a collection of tools and
    libraries for using data in the INSDC Sequence Read Archives.
    This package contains the interface to the VDB."""

    homepage = "https://github.com/ncbi/ncbi-vdb"
    git = "https://github.com/ncbi/ncbi-vdb.git"

    version("3.0.2", tag="3.0.2", commit="c4aa19632714c2f04af07505721fb16c71bba3d5")
    version("3.0.0", tag="3.0.0", commit="2222d7727122d0cbad93344dd6a9044abff34280")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openjdk")
    depends_on("flex@2.6:")
    depends_on("libxml2")
