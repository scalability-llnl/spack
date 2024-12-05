# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Piranha(CMakePackage):
    """Piranha is a computer-algebra library for the symbolic manipulation of
    sparse multivariate polynomials and other closely-related symbolic objects
    (such as Poisson series)."""

    homepage = "https://bluescarni.github.io/piranha/sphinx/"
    url = "https://github.com/bluescarni/piranha/archive/v0.5.tar.gz"
    git = "https://github.com/bluescarni/piranha.git"

    license("LGPL-3.0-or-later")

    version("develop", branch="master")
    version("0.5", sha256="34a89bda8208ff48cfb116efa7d53c09e8a9b3838af4bb96ba2e19e4930b3a58")

    depends_on("cxx", type="build")  # generated

    variant("python", default=True, description="Build the Python bindings")

    # Build dependencies
    depends_on("cmake@3.2.0:", type="build")
    extends("python", when="+python")
    depends_on("python@2.6:", type="build", when="+python")

    # Other dependencies
    depends_on("boost+iostreams+regex+serialization", when="~python")
    depends_on("boost+iostreams+regex+serialization+python", when="+python")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("bzip2")
    depends_on("gmp")  # mpir is a drop-in replacement for this
    depends_on("mpfr")  # Could also be built against mpir

    def cmake_args(self):
        return [self.define_from_variant("BUILD_PYRANHA", "python"), "-DBUILD_TESTS:BOOL=ON"]
