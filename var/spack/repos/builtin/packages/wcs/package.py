# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Wcs(CMakePackage):
    """Simulates whole cell models using discrete event simulation."""

    homepage = "https://github.com/LLNL/wcs.git"
    git = "https://github.com/LLNL/wcs.git"
    maintainers("rblake-llnl")

    license("MIT")

    version("master", branch="master")
    version("develop", branch="devel")

    depends_on("cxx", type="build")  # generated

    depends_on("boost+graph+filesystem+regex+system")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("sbml@5.18.0:+cpp")
    depends_on("cmake@3.12:", type="build")
    depends_on("cereal", type="build")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DBOOST_ROOT:PATH=" + spec["boost"].prefix,
            "-DCEREAL_ROOT:PATH=" + spec["cereal"].prefix,
            "-DSBML_ROOT:PATH=" + spec["sbml"].prefix,
            "-DWCS_WITH_SBML:BOOL=ON",
            "-DWCS_WITH_EXPRTK:BOOL=ON",
        ]
        return args
