# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Aoflagger(CMakePackage):
    """RFI detector and quality analysis
    for astronomical radio observations."""

    homepage = "https://sourceforge.net/projects/aoflagger/"
    url = "https://downloads.sourceforge.net/project/aoflagger/aoflagger-2.10.0/aoflagger-2.10.0.tar.bz2"

    license("GPL-3.0-or-later")

    version("2.10.0", sha256="3ec1188d37101acf2029575ebc09c50b19c158c88a12b55ac5d25a96bd8fc18d")

    depends_on("cxx", type="build")  # generated

    depends_on("casacore+python~fftpack@1.10:")
    depends_on("fftw~mpi@3.0:")
    depends_on("boost+python@:1.66.99")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("libxml2")
    depends_on("lapack")
    depends_on("cfitsio")
